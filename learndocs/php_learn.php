<?php
// PHP Application with common patterns

namespace App\Controllers;  // Define namespace

use PDO;  // Import PDO class
use Exception;  // Import Exception class
use App\Models\User;  // Import User model

class UserController {
    private $db;  // Database connection property
    private $config;  // Configuration array
    
    public function __construct($config) {  // Constructor with dependency
        $this->config = $config;  // Store configuration
        $this->connectDatabase();  // Initialize database connection
    }
    
    private function connectDatabase() {  // Database connection method
        try {
            $dsn = "mysql:host={$this->config['db_host']};dbname={$this->config['db_name']}";  // Build DSN string
            $this->db = new PDO($dsn, $this->config['db_user'], $this->config['db_pass']);  // Create PDO instance
            $this->db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);  // Enable exceptions
        } catch (PDOException $e) {  // Catch connection errors
            error_log("Database connection failed: " . $e->getMessage());  // Log error
            throw new Exception("Database unavailable");  // Throw generic exception
        }
    }
    
    public function createUser($data) {  // Create user method
        // Validate input data
        if (empty($data['email']) || empty($data['password'])) {  // Check required fields
            throw new Exception("Missing required fields");  // Validation error
        }
        
        // Hash password
        $hashedPassword = password_hash($data['password'], PASSWORD_DEFAULT);  // Secure hash
        
        // Prepare SQL statement
        $sql = "INSERT INTO users (email, password, created_at) VALUES (:email, :password, NOW())";  // SQL with placeholders
        $stmt = $this->db->prepare($sql);  // Prepare statement
        
        // Bind parameters
        $stmt->bindParam(':email', $data['email']);  // Bind email parameter
        $stmt->bindParam(':password', $hashedPassword);  // Bind password parameter
        
        // Execute query
        if ($stmt->execute()) {  // Execute and check success
            return $this->db->lastInsertId();  // Return new ID
        }
        
        throw new Exception("User creation failed");  // Operation failed
    }
    
    public function getUser($id) {  // Retrieve user method
        $sql = "SELECT * FROM users WHERE id = :id";  // Select query
        $stmt = $this->db->prepare($sql);  // Prepare statement
        $stmt->bindParam(':id', $id, PDO::PARAM_INT);  // Bind integer parameter
        $stmt->execute();  // Execute query
        
        $user = $stmt->fetch(PDO::FETCH_ASSOC);  // Fetch associative array
        
        if (!$user) {  // Check if found
            return null;  // User not found
        }
        
        unset($user['password']);  // Remove sensitive data
        return $user;  // Return user data
    }
    
    public function updateUser($id, $data) {  // Update user method
        $fields = [];  // Build update fields
        $params = ['id' => $id];  // Parameter array
        
        foreach ($data as $key => $value) {  // Iterate update data
            if (in_array($key, ['email', 'name', 'status'])) {  // Whitelist fields
                $fields[] = "$key = :$key";  // Add to update list
                $params[$key] = $value;  // Add parameter
            }
        }
        
        if (empty($fields)) {  // Check if any updates
            return false;  // Nothing to update
        }
        
        $sql = "UPDATE users SET " . implode(', ', $fields) . " WHERE id = :id";  // Build update query
        $stmt = $this->db->prepare($sql);  // Prepare statement
        
        return $stmt->execute($params);  // Execute with parameters
    }
    
    public function deleteUser($id) {  // Delete user method
        $sql = "DELETE FROM users WHERE id = :id";  // Delete query
        $stmt = $this->db->prepare($sql);  // Prepare statement
        $stmt->bindParam(':id', $id, PDO::PARAM_INT);  // Bind parameter
        
        return $stmt->execute();  // Execute deletion
    }
    
    public function __destruct() {  // Destructor
        $this->db = null;  // Close database connection
    }
}

// Usage example
try {
    $config = require 'config.php';  // Load configuration
    $controller = new UserController($config);  // Instantiate controller
    
    // Create user
    $userId = $controller->createUser([  // Call create method
        'email' => 'user@example.com',
        'password' => 'secure123'
    ]);
    
    // Get user
    $user = $controller->getUser($userId);  // Retrieve user
    print_r($user);  // Display user data
    
} catch (Exception $e) {  // Catch any errors
    echo "Error: " . $e->getMessage();  // Display error message
}