import { Ionicons } from "@expo/vector-icons";
import { Tabs, useRouter } from "expo-router";

export default function TabLayout() {
    const router = useRouter();

    return (
        <Tabs
            screenOptions={{
                headerShown: false, // 헤더에 tsx 내용이 나옴 없애버리고 싶으면 false 
            }}
        >
            <Tabs.Screen // Tabs.Screen 으로 탭의 순서를 정할 수 있음 
                name="index"
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
                        e.preventDefault(); // add.tsx 뜨는 것 방지 
                        router.navigate("/modal"); // modal.tsx 를 찾을 것 -> 부모 _layout 체크 -> 모달 처럼뜨는 옵션 확인 후 모달처럼 렌더링!
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
        </Tabs>
    );
}
