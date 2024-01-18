<template>
  <div>
    <div class="navbar">SPOTIFY PLAYLIST CREATOR</div>
    <div class="login-card centered">
      <button class="login-btn" @click="login">Login with Spotify</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LoginButton',
  methods: {
    checkTokenAndLogin() {
      axios.get('http://localhost:5000/get_token')
        .then(response => {
          if (response.data && response.data.access_token) {
            this.loginWithToken(response.data.access_token);
          } else {
            this.login();
          }
        })
        .catch(error => {
          console.error('Error fetching token:', error);
          this.login();
        });
    },
    loginWithToken(token) {
      localStorage.setItem('spotify_access_token', token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      this.$emit('login-success');
    },

    login() {
      const client_id = '88d09a98f3a342d099d4ee707ded9d89';
      const redirect_uri = encodeURIComponent('http://localhost:5000/callback');
      const scope = encodeURIComponent('user-top-read playlist-modify-private');
      const responseType = 'code';

      const authUrl = `https://accounts.spotify.com/authorize?client_id=${client_id}&redirect_uri=${redirect_uri}&scope=${scope}&response_type=${responseType}`;

      window.location.href = authUrl;
    }
  },
  mounted() {
    this.checkTokenAndLogin();
  }
}
</script>
