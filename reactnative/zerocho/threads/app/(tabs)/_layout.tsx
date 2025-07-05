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
                            if (isLoggedIn) {
                                e.preventDefault();
                                router.navigate("/modal");
                            } else {
                                openLoginModal();
                            }
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
                    listeners={{
                        tabPress: (e) => {
                            if (!isLoggedIn) {
                                e.preventDefault();
                                openLoginModal();
                            }
                        }
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
                        }
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

            <Modal
                visible={isLoginModalOpen}
                transparent={true}
                animationType="slide"
            >
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
