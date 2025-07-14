import { AuthContext } from "@/app/_layout";
import { BlurView } from "expo-blur";
import { usePathname, useRouter } from "expo-router";
import { useContext } from "react";
import { Image, StyleSheet, Text, TouchableOpacity, View } from "react-native";
import { useSafeAreaInsets } from "react-native-safe-area-context";

export default function Index() {
    const router = useRouter();
    const pathName = usePathname();
    const insets = useSafeAreaInsets();
    const { user } = useContext(AuthContext);
    const isLoggedIn = !!user;

    console.log("path name : ", pathName);
    console.log("insets : ", insets)

    return (
        // <SafeAreaView style={styles.conatiner}>
        <View style={[styles.conatiner, { paddingTop: insets.top, paddingBottom: insets.bottom }]} >
            <BlurView style={styles.header} intensity={70}>
                <Image source={require("../../../assets/images/react-logo.png")}></Image>
                {isLoggedIn && <TouchableOpacity style={styles.loginButton} onPress={() => router.navigate(`/login`)}>
                    <Text style={styles.loginButtonText}>로그인</Text>
                </TouchableOpacity>}
            </BlurView>
            {isLoggedIn ??
                <View style={styles.tabContainer}>
                    <View style={styles.tab}>
                        <TouchableOpacity onPress={() => router.push(`/`)}>
                            <Text style={{ color: pathName === "/" ? "red" : "black" }}>For you </Text>
                        </TouchableOpacity>
                    </View>
                    <View style={styles.tab}>
                        <TouchableOpacity onPress={() => router.push(`/following`)}>
                            <Text style={{ color: pathName === "/" ? "black" : "red" }}>Following </Text>
                        </TouchableOpacity>
                    </View>
                </View>}
            {/* </SafeAreaView > */}
            {isLoggedIn ??
                <>
                    <View>
                        <TouchableOpacity onPress={() => router.push(`/@lotto/post/1`)}>
                            <Text>게시글1 </Text>
                        </TouchableOpacity>
                    </View>
                    <View>
                        <TouchableOpacity onPress={() => router.push(`/@lotto/post/2`)}>
                            <Text>게시글2 </Text>
                        </TouchableOpacity>
                    </View>
                    <View>
                        <TouchableOpacity onPress={() => router.push(`/@lotto/post/3`)}>
                            <Text>게시글3 </Text>
                        </TouchableOpacity>
                    </View>
                </>
            }
        </View>
    );
}

const styles = StyleSheet.create({
    conatiner: {
        flex: 1
    },
    tabContainer: {
        flexDirection: "row"
    },
    tab: {
        flex: 1,
        alignItems: "center"
    },
    header: {
        alignItems: "center"
    },
    headerLogo: {
        width: 42,
        height: 42
    },
    loginButton: {
        position: "absolute",
        backgroundColor: "black",
        right: 20,
        top: 0,
        borderWidth: 1,
        borderColor: "black",
        paddingHorizontal: 10,
        paddingVertical: 10,
        borderRadius: 10,
    },
    loginButtonText: {
        color: "white"
    }
})
