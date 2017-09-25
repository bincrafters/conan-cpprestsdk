/**
 * \file
 * \brief List network card and collect information
 *
 * Copyright 2017 Uilian Ries <uilianries@gmail.com>
 */
#define CATCH_CONFIG_MAIN
#include "catch.hpp"


#include <cpprest/version.h>
#include <cpprest/json.h>
#include <cpprest/ws_client.h>

TEST_CASE( "CppRestSDK Version", "[version]" ) {
    REQUIRE(9 == CPPREST_VERSION_MINOR);
    REQUIRE(2 == CPPREST_VERSION_MAJOR);
    REQUIRE(0 == CPPREST_VERSION_REVISION);
}

TEST_CASE( "CppRestSDK JSON", "[json]" ) {
    const int expected_value = -22;
    const auto parsed_value = web::json::value::parse(U("-22"));
    REQUIRE(parsed_value.is_number());
    REQUIRE(expected_value == parsed_value.as_integer());
}

TEST_CASE( "CppRestSDK WebSocket", "[websocket]" ) {
    web::websockets::client::websocket_client_config config;
    web::credentials expected_cred(U("username"), U("password"));

    config.set_credentials(expected_cred);
    web::websockets::client::websocket_client client(config);

    const web::websockets::client::websocket_client_config& config2 = client.config();
    REQUIRE(config2.credentials().username() == expected_cred.username());
}
