<template>
  <div id="app">
    <transition name="zoom" mode="out-in">
      <div key="transition-wrapper">
        <LoginButton @login-success="handleLogin" />
        <PlaylistCreator v-if="isLoggedIn && !playlistCreated" @playlist-created="handlePlaylistCreated" />
        <ValidatePage v-if="playlistCreated" @return-to-creator="resetView" />
      </div>
    </transition>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  name: 'LoginButton',
  methods: {
    initiateLogin() {
      const storedToken = localStorage.getItem('spotify_access_token');
      if (storedToken) {
        this.loginWithToken(storedToken);
      } else {
        this.redirectToSpotifyLogin();
      }
    },
    loginWithToken(token) {
      localStorage.setItem('spotify_access_token', token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      this.$emit('login-success');
    },
    mounted() {
      this.checkTokenAndLogin();
    },

    redirectToSpotifyLogin() {
      const client_id = '88d09a98f3a342d099d4ee707ded9d89';
      const redirect_uri = encodeURIComponent('http://localhost:5000/callback');
      const scope = 'user-top-read playlist-modify-private';
      const responseType = 'code';
      const authUrl = `https://accounts.spotify.com/authorize?client_id=${client_id}&redirect_uri=${redirect_uri}&scope=${scope}&response_type=${responseType}`;
      window.location.href = authUrl;
    }
  }
}
</script>
