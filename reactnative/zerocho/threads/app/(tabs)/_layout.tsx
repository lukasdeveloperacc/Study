import { Ionicons } from "@expo/vector-icons";
import { Tabs, useRouter } from "expo-router";

export default function TabLayout() {
    const router = useRouter();

    return (
        <Tabs
            screenOptions={{
                headerShown: false,
            }}
        >
            <Tabs.Screen
                name="(home)"
                options={{
                    tabBarLabel: () => null,
                    tabBarIcon: ({ focused }) => (
                        <Ionicons
                            name="home"
                            size={24}
                            color={focused ? "black" : "gray"}
                        />
                    ),
                }}
            />
            <Tabs.Screen
                name="search"
                options={{
                    tabBarLabel: () => null,
                    tabBarIcon: ({ focused }) => (
                        <Ionicons
                            name="search"
                            size={24}
                            color={focused ? "black" : "gray"}
                        />
                    ),
                }}
            />
            <Tabs.Screen
                name="add"
                listeners={{
                    tabPress: (e) => {
                        e.preventDefault();
                        router.navigate("/modal");
                    },
                }}
                options={{
                    tabBarLabel: () => null,
                    tabBarIcon: ({ focused }) => (
                        <Ionicons name="add" size={24} color={focused ? "black" : "gray"} />
                    ),
                }}
            />
            <Tabs.Screen
                name="activity"
                options={{
                    tabBarLabel: () => null,
                    tabBarIcon: ({ focused }) => (
                        <Ionicons
                            name="heart-outline"
                            size={24}
                            color={focused ? "black" : "gray"}
                        />
                    ),
                }}
            />
            <Tabs.Screen
                name="[username]"
                options={{
                    tabBarLabel: () => null,
                    tabBarIcon: ({ focused }) => (
                        <Ionicons
                            name="person-outline"
                            size={24}
                            color={focused ? "black" : "gray"}
                        />
                    ),
                }}
            />
            <Tabs.Screen
                name="following"
                options={{
                    tabBarLabel: () => null,
                    href: null,
                }}
            />
            <Tabs.Screen
                name="(post)/[username]/post/[postID]"
                options={{
                    href: null
                }}
            />
        </Tabs>
    );
}
