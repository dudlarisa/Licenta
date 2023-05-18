package com.example.PricePrediction.repositories;

import com.example.PricePrediction.entities.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;
import java.util.UUID;

public interface UserRepository extends JpaRepository<User, UUID>
{
    //Find by email:
    Optional<User> findByEmail(String email);
}
