// ===================================================================
// File: _layout.tsx
// Lokasi: Frontend/app/_layout.tsx
// Deskripsi: File ini adalah layout root atau titik masuk utama untuk
//            seluruh aplikasi. Ia menggantikan fungsi App.js dan AppNavigator.js.
// ===================================================================

import React, { useContext, useEffect } from 'react';
import { Stack, useRouter, useSegments } from 'expo-router';
import { AuthContext, AuthProvider } from '../services/AuthContext';
import { ActivityIndicator, View, StyleSheet } from 'react-native';

// Komponen layout utama yang akan menentukan layar mana yang ditampilkan.
const RootLayout = () => {
  const { authenticated, isLoading } = useContext(AuthContext);
  const segments = useSegments();
  const router = useRouter();

  useEffect(() => {
    if (isLoading) return; // Jangan lakukan apa-apa jika masih loading

    // Menggunakan 'as string' untuk memberi tahu TypeScript agar tidak terlalu ketat
    // dalam memeriksa tipe data segmen saat ini.
    const inAuthGroup = (segments[0] as string) === '(auth)';

    if (authenticated && inAuthGroup) {
      // Jika pengguna sudah login tapi masih di halaman auth,
      // arahkan ke halaman utama.
      router.replace('/(tabs)');
    } else if (!authenticated && !inAuthGroup) {
      // Jika pengguna belum login dan tidak di halaman auth,
      // paksa arahkan ke halaman login.
      // Menggunakan 'as any' untuk melewati pemeriksaan tipe rute sementara.
      router.replace('/(auth)/login' as any);
    }
  }, [authenticated, isLoading, segments]);

  // Tampilkan layar loading saat aplikasi sedang memeriksa token
  if (isLoading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#34A853" />
      </View>
    );
  }

  return (
    <Stack>
      {/* Layar-layar ini tidak memiliki header */}
      <Stack.Screen name="(auth)" options={{ headerShown: false }} />
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
    </Stack>
  );
};

// Komponen utama yang diekspor
export default function AppLayout() {
  return (
    <AuthProvider>
      <RootLayout />
    </AuthProvider>
  );
}

const styles = StyleSheet.create({
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
});
