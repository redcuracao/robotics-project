import { initializeApp } from 'firebase/app'
import { getDatabase } from 'firebase/database'

const firebaseConfig = {
  apiKey: 'AIzaSyBRn3SRzqoOCIsBE9eJBe8RZjuUOCNK-Xw',
  authDomain: 'bottail.firebaseapp.com',
  databaseURL: 'https://bottail-default-rtdb.asia-southeast1.firebasedatabase.app/',
  projectId: 'bottail',
  storageBucket: 'bottail.firebasestorage.app',
  messagingSenderId: '35087707272',
  appId: '1:35087707272:web:937fe5a6de6536475a033d',
}

const app = initializeApp(firebaseConfig)
export const database = getDatabase(app)
