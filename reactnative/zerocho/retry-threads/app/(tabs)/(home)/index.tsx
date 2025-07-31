import Post, { type Post as PostType } from "@/components/Post";
import { FlashList } from "@shopify/flash-list";
import * as Haptics from "expo-haptics";
import { usePathname } from "expo-router";
import { useCallback, useContext, useRef, useState } from "react";
// Pan : drag 하는 행위
import { PanResponder, StyleSheet, useColorScheme, View } from "react-native";
import Animated, {
    useAnimatedScrollHandler,
    useAnimatedStyle,
    useSharedValue,
    withTiming,
} from "react-native-reanimated";
import { AnimationContext } from "./_layout";

// Animated가 가능한 FlashList로 만들어준다.
const AnimatedFlashList = Animated.createAnimatedComponent(FlashList<PostType>);

export default function Index() {
    const colorScheme = useColorScheme();
    const path = usePathname();
    const [posts, setPosts] = useState<PostType[]>([]);
    // useSharedValue : useRef와 같이 자주 바뀌되, 리렌더링 안되는 값들을 저장
    // js가아니라 ui thread에서 처리함 (native 단에서 사용)
    const scrollPosition = useSharedValue(0);
    const isReadyToRefresh = useSharedValue(false);
    const { pullDownPosition } = useContext(AnimationContext);

    const onEndReached = useCallback(() => {
        console.log("onEndReached", posts.at(-1)?.id);
        fetch(`/posts?cursor=${posts.at(-1)?.id}`)
            .then((res) => res.json())
            .then((data) => {
                if (data.posts.length > 0) {
                    setPosts((prev) => [...prev, ...data.posts]);
                }
            });
    }, [posts, path]);

    const onRefresh = (done: () => void) => {
        setPosts([]); // 리프레싱되는 걸 가시적으로 보여주기 위한 용도
        Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
        fetch("/posts")
            .then((res) => res.json())
            .then((data) => {
                setPosts(data.posts);
            })
            .finally(() => {
                done();
            });
    };

    const onPanRelease = () => {
        pullDownPosition.value = withTiming(isReadyToRefresh.value ? 60 : 0, {
            duration: 180,
        });
        console.log("onPanRelease", isReadyToRefresh.value);
        if (isReadyToRefresh.value) {
            onRefresh(() => {
                // withTiming : 천천히 작동시킴
                pullDownPosition.value = withTiming(0, {
                    duration: 180,
                });
            });
        }
    };

    const panResponderRef = useRef(
        PanResponder.create({
            onMoveShouldSetPanResponder: () => true,
            onPanResponderMove: (event, gestureState) => {
                const max = 120; // 120 까지만 당겨진다.
                pullDownPosition.value = Math.max(Math.min(gestureState.dy, max), 0);
                console.log("pull", pullDownPosition.value);

                if (
                    pullDownPosition.value >= max / 2 &&
                    isReadyToRefresh.value === false
                ) {
                    isReadyToRefresh.value = true;
                }
                if (
                    pullDownPosition.value < max / 2 &&
                    isReadyToRefresh.value === true
                ) {
                    isReadyToRefresh.value = false;
                }
            },
            onPanResponderRelease: onPanRelease,
            onPanResponderTerminate: onPanRelease,
        })
    );

    const scrollHandler = useAnimatedScrollHandler({
        onScroll: (event) => {
            console.log("onScroll", event.contentOffset.y);
            scrollPosition.value = event.contentOffset.y;
        },
    });

    const pullDownStyles = useAnimatedStyle(() => {
        return {
            transform: [
                {
                    translateY: pullDownPosition.value,
                },
            ],
        };
    });

    return (
        <Animated.View
            style={[
                styles.container,
                colorScheme === "dark" ? styles.containerDark : styles.containerLight,
                pullDownStyles,
            ]}
            {...panResponderRef.current.panHandlers}
        >
            <AnimatedFlashList
                refreshControl={<View />}
                data={posts}
                nestedScrollEnabled={true}
                onScroll={scrollHandler}
                scrollEventThrottle={16}
                renderItem={({ item }) => <Post item={item} />}
                onEndReached={onEndReached}
                onEndReachedThreshold={2}
                estimatedItemSize={350}
            />
        </Animated.View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
    },
    containerLight: {
        backgroundColor: "white",
    },
    containerDark: {
        backgroundColor: "#101010",
    },
    textLight: {
        color: "black",
    },
    textDark: {
        color: "white",
    },
});
