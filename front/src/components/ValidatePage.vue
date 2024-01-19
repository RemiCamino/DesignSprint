<template>
  <div class="validate-container">
    <div class="navbar">SHUFFLE</div>
    <div class="validate-message">
      Votre Playlist a été créée !
    </div>
    <button @click="goBack" class="return-button">Retour</button>
  </div>
</template>

<script>
export default {
  name: 'ValidatePage',
  methods: {
    goBack() {
      this.$emit('return-to-creator'); // Emit an event instead of routing
    }
  }
}
</script>

<style>
.validate-container {
  text-align: center;
  color: white;
  font-family: Arial, sans-serif;
}

.validate-message {
  margin-top: 20px;
}

.return-button {
  background-color: #1DB954;
  color: white;
  padding: 10px 20px;
  margin-top: 10px;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.return-button:hover {
  background-color: #148f36;
}

.navbar {
  background-color: #000;
  color: #fff;
  padding: 10px 0;
  font-size: 1.5em;
  text-align: center;
}
</style>