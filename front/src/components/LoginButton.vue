<template>
  <div>
    <div class="navbar">SPOTIFY PLAYLIST CREATOR</div>
    <div class="login-card centered">
      <button class="login-btn" @click="login">Login with Spotify</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoginButton',
  methods: {
    login() {
      const client_id = '88d09a98f3a342d099d4ee707ded9d89';
      const redirect_uri = encodeURIComponent('http://localhost:5000/callback');
      const scope = encodeURIComponent('user-top-read playlist-modify-private');
      const responseType = 'code';

      const authUrl = `https://accounts.spotify.com/authorize?client_id=${client_id}&redirect_uri=${redirect_uri}&scope=${scope}&response_type=${responseType}`;

      window.location.href = authUrl;
    }
  }
}
</script>