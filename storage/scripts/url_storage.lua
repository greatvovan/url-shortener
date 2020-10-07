#!/usr/bin/env tarantool
require 'storage_init'
require 'storage_functions'


box.cfg{
    memtx_memory = 1024 * 1024 * 1024
}
print('Starting...')
