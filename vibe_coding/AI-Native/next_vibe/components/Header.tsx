export default function Header() {
  return (
    <header className="w-full bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* 로고 */}
          <div className="flex-shrink-0">
            <h1 className="text-2xl font-bold text-gray-900">
              My Awesome Site
            </h1>
          </div>

          {/* 가입하기 버튼 */}
          <div>
            <button className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-md shadow-md">
              가입하기
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
