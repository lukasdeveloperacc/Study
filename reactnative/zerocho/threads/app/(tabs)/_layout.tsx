import { Ionicons } from "@expo/vector-icons";
import { type BottomTabBarButtonProps } from "@react-navigation/bottom-tabs";
import { Tabs, usePathname, useRouter } from "expo-router";
import { useContext, useRef, useState } from "react";
import {
    Animated,
    Modal,
    Pressable,
    Text,
    TouchableOpacity,
    View,
} from "react-native";
import { AuthContext } from "../_layout";
import { useColorScheme } from "react-native";
const AnimatedTabBarButton = ({
    children,
    onPress,
    style,
    ...restProps
}: BottomTabBarButtonProps) => {
    const scaleValue = useRef(new Animated.Value(1)).current;

    const handlePressOut = () => {
        Animated.sequence([
            Animated.spring(scaleValue, {
                toValue: 1.2,
                useNativeDriver: true,
                speed: 200,
            }),
            Animated.spring(scaleValue, {
                toValue: 1,
                useNativeDriver: true,
                speed: 200,
            }),
        ]).start();
    };

    return (
        <Pressable
            {...restProps}
            onPress={onPress}
            onPressOut={handlePressOut}
            style={[
                { flex: 1, justifyContent: "center", alignItems: "center" },
                style,
            ]}
            // Disable Android ripple effect
            android_ripple={{ borderless: false, radius: 0 }}
        >
            <Animated.View style={{ transform: [{ scale: scaleValue }] }}>
                {children}
            </Animated.View>
        </Pressable>
    );
};

export default function TabLayout() {
    const router = useRouter();
    const { user } = useContext(AuthContext);
    const isLoggedIn = !!user;
    const colorScheme = useColorScheme();
    const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);
    const pathname = usePathname();

    const openLoginModal = () => {
        setIsLoginModalOpen(true);
    };

    const closeLoginModal = () => {
        setIsLoginModalOpen(false);
    };

    const toLoginPage = () => {
        setIsLoginModalOpen(false);
        router.push("/login");
    };

    return (
        <>
            <Tabs
                backBehavior="history"
                screenOptions={{
                    headerShown: false,
                    tabBarButton: (props) => <AnimatedTabBarButton {...props} />,
                    tabBarStyle: {
                        backgroundColor: colorScheme === "dark" ? "#101010" : "white",
                        shadowColor: "transparent",
                        position: "relative",
                    },
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
                                color={focused ? colorScheme === "dark" ? "white" : "black" : "gray"}
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
                                color={focused ? colorScheme === "dark" ? "white" : "black" : "gray"}
                            />
                        ),
                    }}
                />
                <Tabs.Screen
                    name="add"
                    listeners={{
                        tabPress: (e) => {
                            console.log("tabPress");
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
                                color={focused ? colorScheme === "dark" ? "white" : "black" : "gray"}
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
                                color={focused ? colorScheme === "dark" ? "white" : "black" : "gray"}
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
                            } else {
                                router.navigate(`/@${user?.id}`)
                            }
                        },
                    }}
                    options={{
                        tabBarLabel: () => null,
                        tabBarIcon: ({ focused }) => (
                            <Ionicons
                                name="person-outline"
                                size={24}
                                color={focused && user?.id === pathname?.slice(2) ? colorScheme === "dark" ? "white" : "black" : "gray"}
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
                        <Pressable onPress={toLoginPage}>
                            <Text>Login Modal</Text>
                        </Pressable>
                        <TouchableOpacity onPress={closeLoginModal}>
                            <Ionicons name="close" size={24} color="#555" />
                        </TouchableOpacity>
                    </View>
                </View>
            </Modal>
        </>
    );
}
