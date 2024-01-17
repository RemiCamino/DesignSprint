<template>
    <div>
      <div class="navbar">SPOTIFY PLAYLIST CREATOR</div>
      <div class="login-card centered">
        <input type="text" class="input-field" placeholder="Username" />
        <input type="password" class="input-field" placeholder="Password" />
        <button class="login-btn" @click="login">Se Connecter</button>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'LoginButton',
    methods: {
      login() {
        // Since we're simulating the login, we just emit the login-success event.
        this.$emit('login-success');
      }
    }
  }
  </script>
  