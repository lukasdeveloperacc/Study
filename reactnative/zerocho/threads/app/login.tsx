import { Redirect, router } from "expo-router";
import {
    View,
    Text,
    Pressable,
    StyleSheet,
    Alert,
    useColorScheme,
    Platform,
} from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";
import { AuthContext } from "./_layout";
import { useContext, useEffect } from "react";
import { getKeyHashAndroid, initializeKakaoSDK } from "@react-native-kakao/core"
import { login as kakaoLogin, me } from "@react-native-kakao/user"
import * as AppleAuthentication from "expo-apple-authentication"
import Constants from "expo-constants";

export default function Login() {
    const colorScheme = useColorScheme();
    const insets = useSafeAreaInsets();
    const { user, login } = useContext(AuthContext);
    const isLoggedIn = !!user;

    if (isLoggedIn) {
        return <Redirect href="/(tabs)" />;
    }

    useEffect(() => {
        console.log("NATIVE KEY : ", Constants.expoConfig?.extra?.kakaoNativeKey);
        initializeKakaoSDK(Constants.expoConfig?.extra?.kakaoNativeKey as string);
    }, []);

    const onAppleLogin = async () => {
        try {
            const credential = await AppleAuthentication.signInAsync({
                requestedScopes: [
                    AppleAuthentication.AppleAuthenticationScope.FULL_NAME,
                    AppleAuthentication.AppleAuthenticationScope.EMAIL,
                ],
            });
            console.log(credential);
        } catch (error) {
            console.error(error);
        }
    };

    const onKakaoLogin = async () => {
        try {
            console.log("key: ", await getKeyHashAndroid());
            const result = await kakaoLogin();
            console.log(result);
            const user = await me();
            console.log(user);
            // TODO: save the token to server 
            // TODO: save the user token to AsyncStorage, SecureStore from server
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <View
            style={{
                flex: 1,
                justifyContent: "center",
                alignItems: "center",
                paddingTop: insets.top,
                backgroundColor: colorScheme === "dark" ? "black" : "white",
            }}
        >
            <Pressable onPress={() => router.back()}>
                <Text>Back</Text>
            </Pressable>
            <Pressable style={styles.loginButton} onPress={login}>
                <Text style={styles.loginButtonText}>Login</Text>
            </Pressable>
            <Pressable style={styles.kakaoLoginButton} onPress={onKakaoLogin}>
                <Text style={styles.kakaoLoginButtonText}>KakaoLogin</Text>
            </Pressable>
            {Platform.OS === "ios" && <Pressable style={styles.appleLoginButton} onPress={onAppleLogin}>
                <Text style={styles.appleLoginButtonText}>Apple Login</Text>
            </Pressable>}
        </View>
    );
}

const styles = StyleSheet.create({
    loginButton: {
        backgroundColor: "blue",
        padding: 10,
        borderRadius: 5,
        width: 100,
        alignItems: "center",
    },
    loginButtonText: {
        color: "white",
    },
    kakaoLoginButton: {
        backgroundColor: "yellow",
        padding: 10,
        borderRadius: 5,
        width: 100,
        alignItems: "center",
    },
    kakaoLoginButtonText: {
        color: "black",
    },
    appleLoginButton: {
        backgroundColor: "black",
        padding: 10,
        borderRadius: 5,
        width: 100,
        alignItems: "center",
    },
    appleLoginButtonText: {
        color: "white",
    },
});
