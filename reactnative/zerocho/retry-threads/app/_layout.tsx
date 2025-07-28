import { Stack } from "expo-router";

export default function RootLayout() {
  // 적어 주지 않더라도 expo router가 파일 기반으로 Screen을 생성해놔준다.
  // Custom이 필요한 경우에만 따로 작성해준다고 보면된다. ex) modal
  return (
    <Stack screenOptions={{ headerShown: false }}>
      <Stack.Screen name="modal" options={{ presentation: "modal" }} /> {/* presentation: "modal" 모달로 띄우기 Stack에서만 된다.*/}
    </Stack>
  );
}
