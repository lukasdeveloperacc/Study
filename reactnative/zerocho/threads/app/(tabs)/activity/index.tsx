import { NotFound } from "@/app/+not-found";
import { usePathname, useRouter } from "expo-router";
import { Text, TouchableOpacity, View } from "react-native";

export default function Index() {
    const router = useRouter();
    const pathname = usePathname();

    // Define allowed routes for this activity tab
    const allowedRoutes = [
        "/activity",
        "/activity/followers",
        "/activity/replies",
        "/activity/mentions",
        "/activity/quotes",
        "/activity/reposts",
        "/activity/verified"
    ];
    if (!allowedRoutes.includes(pathname)) {
        return <NotFound />
    }

    return (
        <View
            style={{
                flex: 1,
                justifyContent: "center",
                alignItems: "center",
            }}
        >
            <View>
                <TouchableOpacity onPress={() => router.replace(`/activity`)}>
                    <Text>All</Text>
                </TouchableOpacity>
            </View>
            <View>
                <TouchableOpacity onPress={() => router.replace(`/activity/followers`)}>
                    <Text>Followers </Text>
                </TouchableOpacity>
            </View>
            <View>
                <TouchableOpacity onPress={() => router.replace(`/activity/replies`)} >
                    <Text>Replies</Text>
                </TouchableOpacity>
            </View>
            <View>
                <TouchableOpacity onPress={() => router.replace(`/activity/mentions`)} >
                    <Text>Mentions</Text>
                </TouchableOpacity>
            </View>
            <View>
                <TouchableOpacity onPress={() => router.replace(`/activity/quotes`)} >
                    <Text>Quotes</Text>
                </TouchableOpacity>
            </View>
            <View>
                <TouchableOpacity onPress={() => router.replace(`/activity/reposts`)}>
                    <Text>
                        Reposts
                    </Text>
                </TouchableOpacity>
            </View>
            <View>
                <TouchableOpacity onPress={() => router.replace(`/activity/verified`)}>
                    <Text>
                        Verified
                    </Text>
                </TouchableOpacity>
            </View>
        </View>
    );
}
