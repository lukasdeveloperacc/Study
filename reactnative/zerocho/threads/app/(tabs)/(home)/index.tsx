import { usePathname, useRouter } from "expo-router";
import { Text, TouchableOpacity, View, StyleSheet } from "react-native";
import { SafeAreaView, useSafeAreaInsets } from "react-native-safe-area-context";

export default function Index() {
    const router = useRouter();
    const pathName = usePathname();
    const insets = useSafeAreaInsets();

    console.log("path name : ", pathName);
    console.log("insets : ", insets)

    return (
        // <SafeAreaView style={styles.conatiner}>
        <View style={[styles.conatiner, { paddingTop: insets.top, paddingBottom: insets.bottom }]} >
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
                <View style={styles.tab}>
                    <TouchableOpacity onPress={() => router.push(`/@lotto/post/1`)}>
                        <Text>게시글1 </Text>
                    </TouchableOpacity>
                </View>
                <View style={styles.tab}>
                    <TouchableOpacity onPress={() => router.push(`/@lotto/post/2`)}>
                        <Text>게시글2 </Text>
                    </TouchableOpacity>
                </View>
                <View style={styles.tab}>
                    <TouchableOpacity onPress={() => router.push(`/@lotto/post/3`)}>
                        <Text>게시글3 </Text>
                    </TouchableOpacity>
                </View>
            </View>
            {/* </SafeAreaView > */}
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
        flex: 1
    }
})
