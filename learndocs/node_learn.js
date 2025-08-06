// Node.js Express API Example with common patterns

const express = require('express');  // Import web framework
const bodyParser = require('body-parser');  // Parse request bodies
const cors = require('cors');  // Enable cross-origin requests
const morgan = require('morgan');  // HTTP request logger

const app = express();  // Initialize Express application
const PORT = process.env.PORT || 3000;  // Use environment port or default

// Middleware setup
app.use(cors());  // Allow all origins
app.use(bodyParser.json());  // Parse JSON bodies
app.use(bodyParser.urlencoded({ extended: true }));  // Parse URL-encoded bodies
app.use(morgan('combined'));  // Log requests in Apache format

// Database connection (mock)
const db = require('./database');  // Import database module
db.connect()  // Establish connection
  .then(() => console.log('Database connected'))  // Success handler
  .catch(err => console.error('DB connection failed:', err));  // Error handler

// Route definitions
app.get('/health', (req, res) => {  // Health check endpoint
  res.json({ status: 'healthy', timestamp: Date.now() });  // Return JSON response
});

app.post('/api/users', async (req, res) => {  // Create user endpoint
  try {
    const { email, password } = req.body;  // Destructure request body
    
    if (!email || !password) {  // Validate required fields
      return res.status(400).json({ error: 'Missing fields' });  // Bad request
    }
    
    const user = await db.users.create({ email, password });  // Create in database
    res.status(201).json(user);  // Return created resource
  } catch (error) {
    console.error('User creation failed:', error);  // Log error
    res.status(500).json({ error: 'Internal server error' });  // Server error
  }
});

app.get('/api/users/:id', async (req, res) => {  // Get user by ID
  const userId = req.params.id;  // Extract route parameter
  const user = await db.users.findById(userId);  // Query database
  
  if (!user) {  // Check existence
    return res.status(404).json({ error: 'User not found' });  // Not found
  }
  
  res.json(user);  // Return user data
});

// Error handling middleware
app.use((err, req, res, next) => {  // Global error handler
  console.error(err.stack);  // Log stack trace
  res.status(500).send('Something broke!');  // Generic error response
});

// Start server
app.listen(PORT, () => {  // Bind to port
  console.log(`Server running on port ${PORT}`);  // Startup message
});

module.exports = app;  // Export for testing