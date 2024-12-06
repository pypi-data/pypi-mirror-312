#[[
SPDX-License-Identifier: MIT
SPDX-FileCopyrightText: Copyright 2023 Mikhail Svetkin
SPDX-FileCopyrightText: Copyright 2024 msclock
]]

include_guard(GLOBAL)

cmake_minimum_required(VERSION 3.25)

get_property(IN_TRY_COMPILE GLOBAL PROPERTY IN_TRY_COMPILE)

if(IN_TRY_COMPILE)
  return()
endif()

unset(IN_TRY_COMPILE)

# Load the common settings
include(${CMAKE_CURRENT_LIST_DIR}/scripts/build_type.cmake)

# Vcpkg build environment
file(READ ${CMAKE_SOURCE_DIR}/vcpkg.json _vcpkg_json)
string(JSON _builtin_baseline GET ${_vcpkg_json} builtin-baseline)

# Respect environment variable VCPKG_ROOT and VCPKG_INSTALLATION_ROOT if set
if(DEFINED ENV{VCPKG_ROOT} AND NOT "$ENV{VCPKG_ROOT}" STREQUAL "")
  set(_VCPKG_ROOT
      "$ENV{VCPKG_ROOT}"
      CACHE PATH "Vcpkg root directory" FORCE)
elseif(DEFINED ENV{VCPKG_INSTALLATION_ROOT}
       AND NOT "$ENV{VCPKG_INSTALLATION_ROOT}" STREQUAL "")
  set(_VCPKG_ROOT
      "$ENV{VCPKG_INSTALLATION_ROOT}"
      CACHE PATH "Vcpkg root directory" FORCE)
else()
  unset(_VCPKG_ROOT CACHE)
endif()

include(${CMAKE_CURRENT_LIST_DIR}/bootstrap/vcpkg-config.cmake)

set(VCPKG_VERBOSE
    ON
    CACHE BOOL "Vcpkg VCPKG_VERBOSE")

vcpkg_configure(CACHE_DIR_NAME cppcheck-wheel REPO
                https://github.com/microsoft/vcpkg.git REF ${_builtin_baseline})
