package com.example.PricePrediction.controllers;

import com.example._Buzila_Andra_Court_Reserve_Backend.dtos.AddUserDTO;
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
@RequestMapping(value = "/register")
public class RegisterController {

    private final UserService userService;
    private final RoleService roleService;

    @Autowired
    public RegisterController(UserService userService, RoleService roleService)
    {
        this.userService = userService;
        this.roleService = roleService;
    }

    @PostMapping()
    public ResponseEntity<UUID> registerUser(@Valid @RequestBody AddUserDTO addUserDTO)
    {
        //Find role by id:
        Role role = roleService.findEntityRoleByRole("client");

        //Check if the user with email already exists
        User user = userService.findEntityUserByEmail(addUserDTO.getEmail());

        if(user != null)
        {
            return new ResponseEntity<UUID>(user.getId(), HttpStatus.CONFLICT);
        }

        Argon2PasswordEncoder encoder = new Argon2PasswordEncoder(32,64,1,15*1024,2);
        String encodedPassword = encoder.encode(addUserDTO.getPassword());
        addUserDTO.setPassword(encodedPassword);

        //var validPassword = encoder.matches(myPassword, encodedPassword);
        //System.out.println(validPassword);

        //UUID returnat de la insert:
        UUID addUserId = userService.registerUser(addUserDTO, role);

        //Return ID if corect:
        return new ResponseEntity<UUID>(addUserId, HttpStatus.OK);
    }
}
