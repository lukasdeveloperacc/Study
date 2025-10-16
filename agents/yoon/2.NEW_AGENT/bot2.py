from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import datetime, time, timedelta
import re
import pytz
from env import TELEGRAM_BOT_TOKEN
from news_crew import NewsCrew

# 상수 정의
KOREA_TZ = pytz.timezone("Asia/Seoul")
DAILY_INTERVAL_SECONDS = 24 * 60 * 60
MAX_MESSAGE_LENGTH = 3000  # 텔레그램 메시지 분할 기준 (요구사항: 3000자)


def kickoff_crew() -> str:
    """뉴스 크루로부터 뉴스 브리핑을 가져옵니다."""
    news_crew = NewsCrew()
    result = news_crew.crew().kickoff()
    return result.raw


def split_message(text: str, max_length: int = MAX_MESSAGE_LENGTH) -> list[str]:
    """
    긴 메시지를 여러 개의 짧은 메시지로 분할합니다.

    Args:
        text: 분할할 텍스트
        max_length: 최대 메시지 길이 (기본값: 3000)

    Returns:
        분할된 메시지 리스트
    """
    if len(text) <= max_length:
        return [text]

    messages = []
    current_message = ""

    # 줄 단위로 분할하여 처리 (가독성 유지)
    lines = text.split("\n")

    for line in lines:
        # 현재 줄을 추가했을 때 길이가 초과하는지 확인
        if len(current_message + "\n" + line) > max_length:
            # 현재 메시지가 비어있지 않으면 저장
            if current_message:
                messages.append(current_message)
                current_message = ""

            # 한 줄 자체가 너무 긴 경우 강제로 분할
            if len(line) > max_length:
                while len(line) > max_length:
                    messages.append(line[:max_length])
                    line = line[max_length:]
                current_message = line
            else:
                current_message = line
        else:
            # 현재 메시지에 추가
            if current_message:
                current_message += "\n" + line
            else:
                current_message = line

    # 마지막 메시지 저장
    if current_message:
        messages.append(current_message)

    return messages


async def send_long_message(
    context: ContextTypes.DEFAULT_TYPE, chat_id: int, text: str
) -> None:
    """
    긴 텍스트를 여러 메시지로 나누어 전송합니다.
    요구사항: 두 번째 메시지부터 (2/N) 형식으로 페이지 번호 표시

    Args:
        context: 텔레그램 컨텍스트
        chat_id: 채팅 ID
        text: 전송할 텍스트
    """
    messages = split_message(text)
    total_messages = len(messages)

    for i, message in enumerate(messages):
        if i == 0:
            # 첫 번째 메시지
            await context.bot.send_message(
                chat_id=chat_id, text=f"📰 오늘의 뉴스 브리핑:\n\n{message}"
            )
        else:
            # 두 번째 메시지부터 페이지 번호 표시 (2/N 형식)
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"({i+1}/{total_messages})\n\n{message}",
            )


def parse_time_string(time_str: str) -> time:
    """
    HH:MM 형식의 시간 문자열을 파싱합니다.

    Args:
        time_str: HH:MM 형식의 시간 문자열

    Returns:
        time 객체

    Raises:
        ValueError: 형식이 올바르지 않은 경우
    """
    pattern = r"^([0-1]?[0-9]|2[0-3]):([0-5][0-9])$"
    match = re.match(pattern, time_str)

    if not match:
        raise ValueError(
            "시간 형식이 올바르지 않습니다. HH:MM 형식으로 입력해주세요. (예: 09:00)"
        )

    return time(hour=int(match.group(1)), minute=int(match.group(2)))


def calculate_next_run_time(schedule_time: time) -> tuple[datetime, float]:
    """
    다음 실행 시간과 남은 초를 계산합니다 (한국 시간 기준).

    Args:
        schedule_time: 예약 시간

    Returns:
        (다음 실행 시간, 남은 초) 튜플
    """
    now = datetime.now(KOREA_TZ)
    target_time = datetime.combine(now.date(), schedule_time)
    target_time = KOREA_TZ.localize(target_time.replace(tzinfo=None))

    # 현재 시간이 이미 지났다면 다음날로 설정
    if target_time <= now:
        target_time += timedelta(days=1)

    seconds_until = (target_time - now).total_seconds()
    return target_time, seconds_until


def format_time_remaining(seconds: float) -> str:
    """
    남은 시간을 읽기 쉬운 형식으로 포맷합니다.

    Args:
        seconds: 남은 초

    Returns:
        포맷된 시간 문자열 (예: "2시간 30분 후")
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)

    if hours > 0:
        return f"{hours}시간 {minutes}분 후"
    else:
        return f"{minutes}분 후"


# ====================================
# 명령어 핸들러 함수들
# ====================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /start 명령어 핸들러
    봇을 시작하고 사용 가능한 명령어 목록을 안내합니다.
    """
    if not update.message or not update.effective_chat or not update.effective_user:
        return

    welcome_message = (
        f"안녕하세요! 뉴스 브리핑 봇입니다. 📰\n\n"
        f"사용 가능한 명령어:\n\n"
        f"• /get → 즉시 뉴스 브리핑 받기\n"
        f"• /schedule HH:MM → 매일 정해진 시간에 뉴스 예약\n"
        f"   예시: /schedule 09:00\n\n"
        f"• /check → 현재 예약된 스케줄 확인\n"
        f"• /cancel → 예약된 스케줄 취소\n\n"
        f"💡 팁: 언제든지 /get 명령어로 즉시 뉴스를 받아볼 수 있습니다!"
    )

    await update.message.reply_text(welcome_message)


async def get_news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /get 명령어 핸들러
    즉시 뉴스 브리핑을 생성하여 전송합니다.
    """
    if not update.message or not update.effective_chat:
        return

    # 1. 대기 메시지 전송
    await update.message.reply_text(
        "🤖 뉴스 브리핑을 준비하고 있습니다. 잠시만 기다려주세요..."
    )

    try:
        # 2. kickoff_crew() 함수를 호출하여 뉴스 데이터 가져오기
        result = kickoff_crew()
        chat_id = update.effective_chat.id

        # 3. send_long_message 함수를 통해 분할 전송
        await send_long_message(context, chat_id, result)

    except Exception as e:
        await update.message.reply_text(
            f"❌ 뉴스 브리핑을 가져오는 중 오류가 발생했습니다: {str(e)}"
        )


async def set_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /schedule HH:MM 명령어 핸들러
    매일 지정된 시간에 뉴스 브리핑을 보내도록 예약합니다.
    """
    if not update.message or not update.effective_chat:
        return

    if not context.job_queue:
        await update.message.reply_text(
            "❌ 스케줄링 기능을 사용할 수 없습니다. 봇을 다시 시작해주세요."
        )
        return

    # 유효성 검사: 시간 인자 확인
    if not context.args or len(context.args) != 1:
        await update.message.reply_text(
            "⏰ 사용법: /schedule HH:MM\n\n"
            "예시:\n"
            "  /schedule 09:00\n"
            "  /schedule 18:30\n\n"
            "매일 지정된 시간에 뉴스 브리핑을 받을 수 있습니다."
        )
        return

    try:
        # 시간 파싱
        schedule_time = parse_time_string(context.args[0])
        chat_id = update.effective_chat.id

        # 스케줄 관리: 기존 스케줄 제거 (한 사용자당 하나의 스케줄만 허용)
        current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))
        for job in current_jobs:
            job.schedule_removal()

        # 다음 실행 시간 계산
        target_time, seconds_until = calculate_next_run_time(schedule_time)

        # 새 스케줄 설정
        context.job_queue.run_repeating(
            scheduled_news_job,
            interval=DAILY_INTERVAL_SECONDS,
            first=seconds_until,
            chat_id=chat_id,
            name=str(chat_id),
        )

        # 확인 메시지 전송 (다음 실행 시간 및 남은 시간 포함)
        time_remaining = format_time_remaining(seconds_until)
        await update.message.reply_text(
            f"✅ 매일 {schedule_time.strftime('%H:%M')}에 뉴스 브리핑을 보내드리겠습니다!\n\n"
            f"📅 다음 실행: {target_time.strftime('%Y년 %m월 %d일 %H:%M')} (한국시간)\n"
            f"⏰ {time_remaining}"
        )

    except ValueError as e:
        await update.message.reply_text(f"❌ 오류: {str(e)}")
    except Exception as e:
        await update.message.reply_text(
            f"❌ 스케줄 설정 중 오류가 발생했습니다: {str(e)}"
        )


async def check_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /check 명령어 핸들러
    현재 예약된 스케줄을 확인합니다.
    """
    if not update.message or not update.effective_chat or not context.job_queue:
        return

    chat_id = update.effective_chat.id
    current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))

    # 예외 처리: 예약된 스케줄이 없는 경우
    if not current_jobs:
        await update.message.reply_text(
            "📅 예약된 스케줄이 없습니다.\n\n"
            "💡 /schedule HH:MM 명령어로 스케줄을 설정할 수 있습니다."
        )
        return

    # 다음 실행 시간 표시
    for job in current_jobs:
        next_run = job.next_run_time
        if next_run and isinstance(next_run, datetime):
            # 한국 시간으로 변환
            if next_run.tzinfo is None:
                next_run = pytz.UTC.localize(next_run)

            next_run_korea = next_run.astimezone(KOREA_TZ)
            current_time_korea = datetime.now(KOREA_TZ)

            # 남은 시간 계산
            seconds_until = (next_run_korea - current_time_korea).total_seconds()
            time_remaining = format_time_remaining(seconds_until)

            await update.message.reply_text(
                f"📅 현재 예약된 스케줄:\n\n"
                f"🕒 다음 실행: {next_run_korea.strftime('%Y년 %m월 %d일 %H:%M')} (한국시간)\n"
                f"⏰ {time_remaining}"
            )


async def cancel_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /cancel 명령어 핸들러
    현재 예약된 스케줄을 취소합니다.
    """
    if not update.message or not update.effective_chat or not context.job_queue:
        return

    chat_id = update.effective_chat.id
    current_jobs = context.job_queue.get_jobs_by_name(str(chat_id))

    # 예외 처리: 취소할 스케줄이 없는 경우
    if not current_jobs:
        await update.message.reply_text(
            "⚠️ 예약된 스케줄이 없습니다.\n\n"
            "💡 /schedule HH:MM 명령어로 스케줄을 설정할 수 있습니다."
        )
        return

    # 모든 스케줄 취소
    for job in current_jobs:
        job.schedule_removal()

    # 확인 메시지
    await update.message.reply_text(
        "✅ 뉴스 브리핑 스케줄이 취소되었습니다.\n\n"
        "💡 언제든지 /get 명령어로 즉시 뉴스를 받아볼 수 있습니다."
    )


# ====================================
# 스케줄 작업 함수
# ====================================

async def scheduled_news_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    스케줄된 시간에 실행되는 작업
    매일 정해진 시간에 뉴스 브리핑을 전송합니다.
    """
    if not context.job or not context.job.chat_id:
        return

    chat_id = context.job.chat_id

    # 시작 메시지 전송
    await context.bot.send_message(
        chat_id=chat_id, text="🕙 예정된 시간입니다! 뉴스 브리핑을 시작합니다..."
    )

    try:
        # 뉴스 브리핑 가져오기
        result = kickoff_crew()

        # 긴 메시지 분할 전송
        await send_long_message(context, chat_id, result)

    except Exception as e:
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"❌ 뉴스 브리핑을 가져오는 중 오류가 발생했습니다: {str(e)}"
        )


# ====================================
# 메인 실행 함수
# ====================================

def run_bot() -> None:
    """
    텔레그램 봇을 시작합니다.
    """
    # Application 빌드
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # 명령어 핸들러 등록
    handlers = [
        ("start", start),
        ("get", get_news),
        ("schedule", set_schedule),
        ("check", check_schedule),
        ("cancel", cancel_schedule),
    ]

    for command, handler in handlers:
        app.add_handler(CommandHandler(command, handler))

    # 폴링 시작
    print("🤖 봇이 시작되었습니다...")
    app.run_polling()


if __name__ == "__main__":
    run_bot()
