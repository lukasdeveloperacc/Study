import AsyncStorage from "@react-native-async-storage/async-storage";
import { Redirect, router } from "expo-router";
import * as SecureStore from "expo-secure-store";
import { Pressable, StyleSheet, Text, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

export default function Login() {
    const insets = useSafeAreaInsets();
    const isLoggedIn = false;
    if (isLoggedIn) {
        return <Redirect href="/(tabs)" />
    }

    const onLogin = () => {
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
    }

    return (
        <View style={{ paddingTop: insets.top }}>
            <Pressable onPress={() => router.back()}>
                <Text>Back</Text>
            </Pressable>
            <Pressable style={styles.loginButton} onPress={onLogin}>
                <Text style={styles.loginButtonText}>Login</Text>
            </Pressable>
        </View>
    )
}

const styles = StyleSheet.create({
    loginButton: {
        backgroundColor: "blue",
        padding: 10,
        borderRadius: 5,
        width: 100,
        alignItems: "center"
    },
    loginButtonText: {
        color: "white"
    }
})
