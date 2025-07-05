import { useRouter } from "expo-router";
import { View, Text, Pressable } from "react-native";

export default function Modal() {
    const router = useRouter();

    return (
        <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
            <Text>Im a Modal</Text>
            <Pressable onPress={() => router.back()}>
                <Text>Close</Text>
            </Pressable>
        </View>
    )
}
