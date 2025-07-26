import { Stack } from "expo-router";

export default function RootLayout() {
  return (
    <Stack screenOptions={{ headerShown: false }}>
      <Stack.Screen name="modal" options={{ presentation: "modal" }} /> {/* presentation: "modal" 모달로 띄우기 Stack에서만 된다.*/}
    </Stack>
  );
}
