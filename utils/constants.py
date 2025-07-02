error_code_dict = {
    "UNAUTHORIZED_ERROR":{
        "error_code": "AUTH_001",
        "error_message": "Unauthorized user"
    },
    "INACTIVE_USER":{
        "error_code": "AUTH_002",
        "error_message": "Inactive User"
    },
    "INVALID_LOGIN_CREDENTIAL":{
         "error_code": "AUTH_003",
        "error_message": "Invalid login credential"
    },
    "BAD_REQUEST":{
           "error_code": "AUTH_004",
        "error_message": "Bad Request credential"
    },
    "DATABASE_INTEGRITY":{
        "error_code": "AUTH_005",
         "error_message": "Database Integrity"
    },
    "EMPTY_STREET":{
         "error_code": "ERROR_006",
         "error_message": "Street cannot be empty"
    },
    "IMPROPER_STREET":{
         "error_code": "ERROR_007",
         "error_message": "Street must be at least 3 characters long"
    },
    "EMPTY_AREA":{
        "error_code": "ERROR_008",
         "error_message": "Area cannot be empty"
    },
    "IMPROPER_AREA":{
        "error_code": "ERROR_009",
        "error_message": "Area validation failed: less than 3 characters" 
    },
    "IMPROPER_PINCODE":{
         "error_code": "ERROR_010",
        "error_message": "Pincode must be a 6-digit number" 
    },
    "UNSUPPORTED_PINCODE":{
        "error_code": "ERROR_011",
        "error_message": "Invalid or unsupported pincode"
    },
    "ADDRESS_ID_REQUIRED":{
        "error_code": "ERROR_012",
        "error_message": "Address id required"
    },
    "INVALID_ADDRESS_FORMAT":{
        "error_code": "ERROR_013",
        "error_message": "Invalid address format or field"
    },
    "ADDRESS_NOT_PRESENT":{
        "error_code": "ERROR_014",
        "error_message": "Address ID not present"
    },
    "DUPLICATE_EMAIL":{
        "error_code": "ERROR_015",
        "error_message": "Custom user with this email already exists"
    },
    "INVALID_ROLE":{
        "error_code": "ERROR_016",
        "error_message": "Invalid role choice"
    },
    "INVALID_USER_NAME":{
        "error_code": "ERROR_017",
        "error_message": "Name must be at least 3 characters long"
    },
    "INVALID_FOOD_NAME":{
        "error_code": "ERROR_018",
        "error_message": "Invalid food name"
    },
    "INVALID_PRICE":{
        'error_code': "ERROR_019",
        "error_message": 'Invalid price'
    },
    "INACTIVE_CATEGORY":{
        "error_code": "ERROR_020",
        "error_message": "Inactive category"
    },
    "INACTIVE_HOTEL":{
        "error_code": "ERROR_021",
        "error_message": "Inactive hotel"
    },
    "INVALID_FOOD_FIELD_VALUE":{
         "error_code": "ERROR_022",
        "error_message": "Invalid food field value"
    },
    "INVALID_HOTEL_NAME":{
        "error_code": "ERROR_023",
        "error_message": "Invalid hotel name"
    },
    "INACTIVE_ADDRESS":{
        "error_code": "ERROR_024",
        "error_message": "Given address is inactive"
    },
    "HOTEL_WITH_ADDRESS_EXISTS":{
        "error_code": "ERROR_025",
        "error_message": "Hotel with this address exist"
    },
    "INVALID_HOTEL_FIELD_OR_FORMAT":{
        "error_code": "ERROR_026",
        "error_message": "Invalid filter format or field"
    },
    "INVALID_HOTEL_NAME":{
        "error_code": "ERROR_027",
        "error_message": "Invalid hotel_name"
    },
    "INVALID_AREA":{
         "error_code": "ERROR_028",
        "error_message": "Invalid area name"
    },
    "HOTEL_ID_REQUIRED":{
        "error_code": "ERROR_029",
        "error_message": "Hotel id required"
    },
    "NO_HOTEL_FOUND":{
        "error_code": "ERROR_030",
        "error_message": "No hotel found to update"
    }
}