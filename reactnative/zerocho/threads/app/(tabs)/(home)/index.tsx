import { View, StyleSheet, useColorScheme, PanResponder } from "react-native";
import { usePathname } from "expo-router";
import Post, { type Post as PostType } from "@/components/Post";
import { FlashList } from "@shopify/flash-list";
import { useCallback, useRef, useState } from "react";
import * as Haptics from "expo-haptics";
import Animated, { useAnimatedScrollHandler, useAnimatedStyle, useSharedValue, withTiming } from "react-native-reanimated";
import { useContext } from "react";
import { AnimationContext } from "@/app/(tabs)/(home)/_layout";
import Constants from "expo-constants";

const AnimatedFlashList = Animated.createAnimatedComponent(FlashList<PostType>);

export default function Index() {
  const colorScheme = useColorScheme();
  const path = usePathname();
  const [posts, setPosts] = useState<PostType[]>([]);
  const [refreshing, setRefreshing] = useState(false);
  const scrollPosition = useSharedValue(0); // 얼마나 스크롤 됐는지 ?
  const { pullDownPosition } = useContext(AnimationContext);
  const isReadyToRefresh = useSharedValue(false);

  const onEndReached = useCallback(() => {
    console.log("onEndReached", posts.at(-1)?.id);
    fetch(`${__DEV__ ? "" : Constants.expoConfig?.extra?.apiUrl}/posts?cursor=${posts.at(-1)?.id}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.posts.length > 0) {
          setPosts((prev) => [...prev, ...data.posts]);
        }
      });
  }, [posts, path]);

  const onRefresh = useCallback((done?: () => void) => {
    setRefreshing(true);
    setPosts([]); // 임의로 보이는 효과를 위함
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
    fetch(`${__DEV__ ? "" : Constants.expoConfig?.extra?.apiUrl}/posts`)
      .then((res) => res.json())
      .then((data) => {
        setPosts(data.posts);
      })
      .finally(() => {
        done?.();
      });
  }, []);

  const scrollHandler = useAnimatedScrollHandler({
    onScroll: (event) => {
      console.log("onScroll", event.contentOffset.y);
      scrollPosition.value = event.contentOffset.y;
    },
  });

  const onPanRelease = () => {
    pullDownPosition.value = withTiming(isReadyToRefresh.value ? 60 : 0, { duration: 180 });

    if (isReadyToRefresh.value) {
      onRefresh(() => {
        pullDownPosition.value = withTiming(0, { duration: 180 });
      });
    }

  };

  const panResponderRef = useRef(
    PanResponder.create({
      onMoveShouldSetPanResponder: () => true,
      onPanResponderMove: (event, gestureState) => {
        const max = 120;
        pullDownPosition.value = Math.max(Math.min(gestureState.dy, max), 0);
        console.log("Pull", pullDownPosition.value);

        if (pullDownPosition.value > max / 2 && isReadyToRefresh.value === false) {
          isReadyToRefresh.value = true;
        }

        if (pullDownPosition.value < max / 2 && isReadyToRefresh.value === true) {
          isReadyToRefresh.value = false;
        }
      },
      onPanResponderRelease: onPanRelease,
      onPanResponderTerminate: onPanRelease,
    })
  );

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
        pullDownStyles
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
