import AsyncStorage from "@react-native-async-storage/async-storage";
import { router, Stack } from "expo-router";
import * as SecureStore from "expo-secure-store";
import { createContext, useEffect, useState } from "react";

interface User {
  id: string; name: string; description: string; profileImageUrl: string;
}

export const AuthContext = createContext<{ user?: User | null, login?: () => Promise<any>, logout?: () => Promise<any> }>({ user: null });

export default function RootLayout() {
  const [user, setUser] = useState(null);

  const login = () => {
    console.log("login");
    const data = JSON.stringify({
      username: "lotto",
      password: "1234"
    })
    console.log("Data: ", data)
    fetch("/login", {
      method: "POST",
      body: data,
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data)
        setUser(data.user);
        return Promise.all([
          SecureStore.setItem("accessToken", data.accessToken),
          SecureStore.setItem("refreshToken", data.refreshToken),
          AsyncStorage.setItem("user", JSON.stringify(data.user))
        ])
      })
      .then(() => {
        router.push("/(tabs)");
      })
      .catch((error) => console.error(error))
  };

  const logout = () => {
    setUser(null);
    return Promise.all([
      SecureStore.deleteItemAsync("accessToken"),
      SecureStore.deleteItemAsync("refreshToken"),
      AsyncStorage.removeItem("user")
    ])
  };

  useEffect(() => {
    AsyncStorage.getItem("user").then((user) => {
      setUser(user ? JSON.parse(user) : null);
    })
    // TOOD : validation access token
  })

  return (
    <AuthContext value={{ user, login, logout }}>
      <Stack screenOptions={{ headerShown: false }}>
        <Stack.Screen name="(tabs)" />
        <Stack.Screen name="modal" options={{ presentation: "modal" }} />
      </Stack>
    </AuthContext>
  );
}
