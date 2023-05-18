package com.example.PricePrediction.services;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.rest.webmvc.ResourceNotFoundException;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class RoleService {

    private static final Logger LOGGER = LoggerFactory.getLogger(UserService.class);
    private final RoleRepository roleRepository;

    @Autowired
    public RoleService(RoleRepository roleRepository) {
        this.roleRepository = roleRepository;
    }

    public Role findEntityRoleByRole(String role)
    {
        //Find in DB:
        Optional<Role> roleOptional = roleRepository.findByRole(role);

        //If present, log, if not, throw;
        if (!roleOptional.isPresent()) {
            LOGGER.error("Role with role {} was not found in the db!", role);

            throw new ResourceNotFoundException(Role.class.getSimpleName()
                    + " with id: " + role + " was not found!");
        }

        //Return entity court:
        return roleOptional.get();
    }
}
