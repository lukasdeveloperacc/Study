import { Ionicons } from "@expo/vector-icons";
import { Tabs, useRouter } from "expo-router";
import { useState } from "react";
import { Modal, Text, TouchableOpacity, View } from "react-native";

export default function TabLayout() {
    const router = useRouter();
    const isLoggedIn = true;
    const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);

    const openLoginModal = () => {
        setIsLoginModalOpen(true);
    };

    const closeLoginModal = () => {
        setIsLoginModalOpen(false);
    };

    return (
        <>
            <Tabs
                backBehavior="history" /* 기본이 initial Route라 home으로 가버린다.  */
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
                            if (isLoggedIn) {
                                router.navigate("/modal");
                            } else {
                                openLoginModal();
                            }
                        },
                    }}
                    options={{
                        tabBarLabel: () => null,
                        tabBarIcon: ({ focused }) => (
                            <Ionicons
                                name="add"
                                size={24}
                                color={focused ? "black" : "gray"}
                            />
                        ),
                    }}
                />
                <Tabs.Screen
                    name="activity"
                    listeners={{
                        tabPress: (e) => {
                            if (!isLoggedIn) {
                                e.preventDefault();
                                openLoginModal();
                            }
                        },
                    }}
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
                    listeners={{
                        tabPress: (e) => {
                            if (!isLoggedIn) {
                                e.preventDefault();
                                openLoginModal();
                            }
                        },
                    }}
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
                    name="(post)/[username]/post/[postID]"
                    options={{
                        href: null,
                    }}
                />
            </Tabs>
            <Modal
                visible={isLoginModalOpen}
                transparent={true} /* 투명한 배경, 뒷 부분이 보임 */
                animationType="slide" /* 올라 갔다 내렸갔다 하는 형식으로 보임 */
            >
                {/* login modal */}
                <View
                    style={{
                        flex: 1,
                        justifyContent: "flex-end",
                        backgroundColor: "rgba(0, 0, 0, 0.5)",
                    }}
                >
                    <View style={{ backgroundColor: "white", padding: 20 }}>
                        <Text>Login Modal</Text>
                        <TouchableOpacity onPress={closeLoginModal}>
                            <Ionicons name="close" size={24} color="#555" />
                        </TouchableOpacity>
                    </View>
                </View>
            </Modal>
        </>
    );
}
