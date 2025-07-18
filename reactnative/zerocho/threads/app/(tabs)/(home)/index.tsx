import {
  Text,
  View,
  TouchableOpacity,
  StyleSheet,
  useColorScheme,
} from "react-native";
import { useRouter } from "expo-router";
import { AuthContext } from "../../_layout";
import { useContext } from "react";

export default function Index() {
  const router = useRouter();
  const { user } = useContext(AuthContext);
  const isLoggedIn = !!user;
  const colorScheme = useColorScheme();

  return (
    <View style={[styles.container, colorScheme === "dark" ? styles.containerDark : styles.containerLight]} >
      <View>
        <TouchableOpacity onPress={() => router.push(`/@zerocho/post/1`)}>
          <Text style={colorScheme === "dark" ? styles.textDark : styles.textLight}>게시글1</Text>
        </TouchableOpacity>
      </View>
      <View>
        <TouchableOpacity onPress={() => router.push(`/@zerocho/post/2`)}>
          <Text style={colorScheme === "dark" ? styles.textDark : styles.textLight}>게시글2</Text>
        </TouchableOpacity>
      </View>
      <View>
        <TouchableOpacity onPress={() => router.push(`/@zerocho/post/3`)}>
          <Text style={colorScheme === "dark" ? styles.textDark : styles.textLight}>게시글3</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  containerDark: {
    backgroundColor: "black",
  },
  containerLight: {
    backgroundColor: "white",
  },
  textDark: {
    color: "white",
  },
  textLight: {
    color: "black",
  },
});
