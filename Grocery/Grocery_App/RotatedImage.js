import { View, Image, StyleSheet, Dimensions } from 'react-native';
import config from './config';
import {initializeApp, getApps} from 'firebase/app';
import {getStorage, ref, getDownloadURL} from'firebase/storage';
import { getFirestore, doc, onSnapshot } from "firebase/firestore";
import React, {useState, useEffect} from 'react';
 
const app = initializeApp(config);
const db = getFirestore(app);

const { width, height } = Dimensions.get('window');

const RotatedImage = () => {
    const [url, setUrl] = useState();
    //const [time, setTime] = useState();

    useEffect(() => {
        const unsub = onSnapshot(doc(db, "Timestamps", "Timestamp"), (doc) => {
        //setTime(doc.data());
        console.log("Current data: ", doc.data());

        const func = async() => {
            const storage = getStorage();
            const reference = ref(storage, "/image1.png");
            await getDownloadURL(reference).then((x) => {
            setUrl(x);
            })
        }
    
        func();
        });
    }, []);
    
  return (
    <View style={styles.container}>
      <Image
        source={{ uri: url}}
        style={styles.image}
        resizeMode="contain" // Ensure the image maintains its aspect ratio
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  image: {
    width: height, // Fit to the height of the screen (rotated)
    height: width, // Fit to the width of the screen (rotated)
    transform: [{ rotate: '90deg' }], // Rotate 90 degrees
  },
});

export default RotatedImage;
