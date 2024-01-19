<template>
  <div>
    <div class="navbar">
      Bienvenue sur SHUFFLEMAX, {{ username }}
      <button class="logout-btn" @click="logout">Logout</button>
    </div>
    
    <div class="playlist-creator">
      <h3>Create a Playlist</h3>
      <input type="text" v-model="playlistName" placeholder="Enter playlist name..." class="playlist-input">
      <button @click="createPlaylist" class="create-playlist-button">Create Playlist</button>
    </div>

    <ValidatePage v-if="playlistCreated" @return-to-creator="resetView" />
  </div>
</template>

<script>
import ValidatePage from './ValidatePage.vue';
import axios from 'axios';

export default {
  name: 'PlaylistCreator',
  components: {
    ValidatePage
  },
  data() {
    return {
      playlistName: '',
      playlistCreated: false,
      username: '',
    };
  },
  created() {
    this.fetchUserProfile();
  },
  methods: {
    fetchUserProfile() {
      const token = localStorage.getItem('spotify_access_token');
      if (token) {
        axios.get('http://localhost:5000/get_user_profile', {
          headers: { Authorization: `Bearer ${token}` }
        })
        .then(response => {
          this.username = response.data.display_name;
        })
        .catch(error => {
          console.error('Error fetching user profile:', error);
        });
      }
    },
    createPlaylist() {
      const token = localStorage.getItem('spotify_access_token');
      if (this.playlistName.trim() && token) {
        axios.post('http://localhost:5000/create_playlist', {
          playlist_name: this.playlistName
        }, {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          }
        })
        .then(response => {
          console.log(response.data);
          this.playlistCreated = true;
        })
        .catch(error => {
          console.error('Error creating playlist:', error);
        });
      }
    },
    resetView() {
      this.playlistCreated = false;
      this.playlistName = '';
    },
    logout() {
      localStorage.removeItem('spotify_access_token');
      location.reload();
    }
  }
}
</script>

<style>
.navbar {
  background-color: #000;
  color: #fff;
  padding: 15px 0;
  font-size: 2em;
  text-align: center;
  font-family: 'Helvetica Neue', sans-serif; 
  letter-spacing: 1px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  margin-bottom: 20px;
  margin-left: 10px;
}
  
  .genre-buttons {
    margin: 20px;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .genre-button {
    background-color: #1DB954;
    color: white;
    border: none;
    border-radius: 20px;
    margin: 5px;
    padding: 10px 20px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .genre-button:hover {
    background-color: #148f36;
  }
  
  .genre-input {
    margin-top: 20px;
    padding: 10px;
    border-radius: 20px;
    border: 1px solid #ccc;
    width: 80%;
  }
  
  .genre-input::placeholder {
    color: #aaa;
  }

  .playlist-creator {
  text-align: center;
  margin-top: 20px;
}

.playlist-input {
    margin-top: 20px;
    padding: 10px;
    border-radius: 20px;
    border: 1px solid #ccc;
    width: 80%;
}

.create-playlist-button {
  background-color: #1DB954;
  color: white;
  padding: 10px 20px;
  margin-top: 10px;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.create-playlist-button:hover {
  background-color: #148f36;
}

.playlist-creator h3 {
  color: white;
  font-family: Arial, sans-serif;
}

.created-playlist-message {
  color: white;
  font-family: Arial, sans-serif;
}

.logout-btn {
  background-color: red;
  color: white;
  border: none;
  border-radius: 20px;
  padding: 10px 20px;
  cursor: pointer;
  float: right;
  margin-right: 20px;
}

.logout-btn:hover {
  background-color: darkred;
}
  </style>
  