import { usePathname, useRouter } from "expo-router";
import { Text, TouchableOpacity, View } from "react-native";

export default function Index() {
    const router = useRouter();
    const pathName = usePathname();

    console.log("path name : ", pathName);

    return (
        <View
            style={{
                flex: 1,
                justifyContent: "center",
                alignItems: "center",
            }}
        >
            <View>
                <TouchableOpacity onPress={() => router.push(`/`)}>
                    <Text style={{ color: pathName === "/" ? "red" : "black" }}>For you </Text>
                </TouchableOpacity>
                <TouchableOpacity onPress={() => router.push(`/following`)}>
                    <Text style={{ color: pathName === "/" ? "black" : "red" }}>Following </Text>
                </TouchableOpacity>
                <TouchableOpacity onPress={() => router.push(`/@lotto/post/1`)}>
                    <Text>게시글1 </Text>
                </TouchableOpacity>
                <TouchableOpacity onPress={() => router.push(`/@lotto/post/2`)}>
                    <Text>게시글2 </Text>
                </TouchableOpacity>
                <TouchableOpacity onPress={() => router.push(`/@lotto/post/3`)}>
                    <Text>게시글3 </Text>
                </TouchableOpacity>
            </View>
        </View>
    );
}
