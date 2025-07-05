import React, { useEffect, useState } from "react";
import { View, StyleSheet, Text, ScrollView, Dimensions } from "react-native";
import { StatusBar } from "expo-status-bar";
import * as Location from "expo-location"
const { width: SCREEN_WIDTH } = Dimensions.get("window")

const WEATHER_API_KEY = "b10f13c41a8d709be7dfb6bfbb4d47da"
export default function App() {
  const [city, setCity] = useState<string>("Loading...");
  const [days, setDays] = useState<[]>([]);
  const [ok, setOk] = useState(true);
  const ask = async () => {
    const { granted } = await Location.requestForegroundPermissionsAsync();
    if (!granted) {
      setOk(false);
    }

    const { coords: { latitude, longitude } } = await Location.getCurrentPositionAsync({ accuracy: 5 })
    const location = await Location.reverseGeocodeAsync({ latitude, longitude });
    console.log("Location : ", location[0].region);
    setCity(location[0].region ?? "")
  }

  useEffect(() => {
    ask();
  })

  return (
    <View style={styles.container}>
      <StatusBar style="dark" />
      <View style={styles.city}>
        <Text style={styles.cityName}>{city}</Text>
      </View>
      <ScrollView pagingEnabled showsHorizontalScrollIndicator={false} horizontal contentContainerStyle={styles.weather}>
        <View style={styles.day}>
          <Text style={styles.temperature}>27</Text>
          <Text style={styles.description}>Sunny</Text>
        </View>
        <View style={styles.day}>
          <Text style={styles.temperature}>27</Text>
          <Text style={styles.description}>Sunny</Text>
        </View>
        <View style={styles.day}>
          <Text style={styles.temperature}>27</Text>
          <Text style={styles.description}>Sunny</Text>
        </View>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1, backgroundColor: "tomato"
  },
  city: {
    flex: 1.2, justifyContent: "center", alignItems: "center"
  },
  cityName: {
    fontSize: 68, fontWeight: "500"
  },
  weather: {
    // flex: 3
  },
  day: {
    width: SCREEN_WIDTH,
    alignItems: "center"
  },
  temperature: {
    marginTop: 50,
    fontSize: 178
  },
  description: {
    marginTop: -30,
    fontSize: 60
  }
})
