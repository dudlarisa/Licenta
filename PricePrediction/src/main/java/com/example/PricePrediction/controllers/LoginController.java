package com.example.PricePrediction.controllers;

import com.example._Buzila_Andra_Court_Reserve_Backend.dtos.AddUserDTO;
import com.example._Buzila_Andra_Court_Reserve_Backend.dtos.LoginDTO;
import com.example._Buzila_Andra_Court_Reserve_Backend.dtos.ReturnedLoginDTO;
import com.example._Buzila_Andra_Court_Reserve_Backend.entities.Role;
import com.example._Buzila_Andra_Court_Reserve_Backend.entities.User;
import com.example._Buzila_Andra_Court_Reserve_Backend.services.RoleService;
import com.example._Buzila_Andra_Court_Reserve_Backend.services.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.argon2.Argon2PasswordEncoder;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.UUID;

@RestController
@CrossOrigin
@RequestMapping(value = "/login")
public class LoginController {

    private final UserService userService;

    @Autowired
    public LoginController(UserService userService)
    {
        this.userService = userService;
    }

    @PostMapping()
    public ResponseEntity<ReturnedLoginDTO> loginUser(@Valid @RequestBody LoginDTO loginDTO)
    {
        //Check if the user with email already exists
        User user = userService.findEntityUserByEmailLogin(loginDTO.getEmail());

        Argon2PasswordEncoder encoder = new Argon2PasswordEncoder(32,64,1,15*1024,2);

        boolean validPassword = encoder.matches(loginDTO.getPassword(), user.getPassword());
        System.out.println(loginDTO.getPassword() + " " + validPassword);
        System.out.println(encoder.encode(loginDTO.getPassword()));
        if(validPassword)
        {
            ReturnedLoginDTO userLogat = new ReturnedLoginDTO(user.getId(), user.getRole().getRole());
            return new ResponseEntity<ReturnedLoginDTO>(userLogat, HttpStatus.OK);
        }
        else
        {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
    }
}

