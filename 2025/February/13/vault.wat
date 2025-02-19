(module
  (type (;0;) (func (param i32) (result i32)))
  (type (;1;) (func (result i32)))
  (type (;2;) (func))
  (type (;3;) (func (param i32)))
  (type (;4;) (func (param i32 i32 i32) (result i32)))
  (type (;5;) (func (param i32 i32) (result i32)))
  (type (;6;) (func (param i32 i64 i32) (result i64)))
  (func (;0;) (type 2)
    call 14)
  (func (;1;) (type 0) (param i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32)
    global.get 0
    local.set 1
    i32.const 16
    local.set 2
    local.get 1
    local.get 2
    i32.sub
    local.set 3
    local.get 3
    local.get 0
    i32.store offset=12
    local.get 3
    i32.load offset=12
    local.set 4
    local.get 3
    i32.load offset=12
    local.set 5
    local.get 4
    local.get 5
    i32.mul
    local.set 6
    local.get 3
    i32.load offset=12
    local.set 7
    local.get 6
    local.get 7
    i32.add
    local.set 8
    i32.const 2
    local.set 9
    local.get 8
    local.get 9
    i32.rem_s
    local.set 10
    i32.const 0
    local.set 11
    local.get 10
    local.set 12
    local.get 11
    local.set 13
    local.get 12
    local.get 13
    i32.eq
    local.set 14
    i32.const 1
    local.set 15
    local.get 14
    local.get 15
    i32.and
    local.set 16
    local.get 16
    return)
  (func (;2;) (type 0) (param i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32)
    global.get 0
    local.set 1
    i32.const 16
    local.set 2
    local.get 1
    local.get 2
    i32.sub
    local.set 3
    local.get 3
    local.get 0
    i32.store offset=12
    local.get 3
    i32.load offset=12
    local.set 4
    local.get 3
    i32.load offset=12
    local.set 5
    local.get 4
    local.get 5
    i32.mul
    local.set 6
    local.get 3
    i32.load offset=12
    local.set 7
    local.get 6
    local.get 7
    i32.sub
    local.set 8
    i32.const 2
    local.set 9
    local.get 8
    local.get 9
    i32.rem_s
    local.set 10
    i32.const 1
    local.set 11
    local.get 10
    local.set 12
    local.get 11
    local.set 13
    local.get 12
    local.get 13
    i32.eq
    local.set 14
    i32.const 1
    local.set 15
    local.get 14
    local.get 15
    i32.and
    local.set 16
    local.get 16
    return)
  (func (;3;) (type 0) (param i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32)
    global.get 0
    local.set 1
    i32.const 16
    local.set 2
    local.get 1
    local.get 2
    i32.sub
    local.set 3
    local.get 3
    local.get 0
    i32.store offset=12
    local.get 3
    i32.load offset=12
    local.set 4
    i32.const 305419896
    local.set 5
    local.get 4
    local.get 5
    i32.xor
    local.set 6
    local.get 3
    i32.load offset=12
    local.set 7
    i32.const 16
    local.set 8
    local.get 7
    local.get 8
    i32.shr_s
    local.set 9
    local.get 6
    local.get 9
    i32.add
    local.set 10
    local.get 3
    i32.load offset=12
    local.set 11
    i32.const 65535
    local.set 12
    local.get 11
    local.get 12
    i32.and
    local.set 13
    local.get 10
    local.get 13
    i32.sub
    local.set 14
    local.get 14
    return)
  (func (;4;) (type 0) (param i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32)
    global.get 0
    local.set 1
    i32.const 16
    local.set 2
    local.get 1
    local.get 2
    i32.sub
    local.set 3
    local.get 3
    local.get 0
    i32.store offset=12
    local.get 3
    i32.load offset=12
    local.set 4
    i32.const -559038737
    local.set 5
    local.get 4
    local.get 5
    i32.mul
    local.set 6
    local.get 3
    i32.load offset=12
    local.set 7
    i32.const -889275714
    local.set 8
    local.get 7
    local.get 8
    i32.add
    local.set 9
    local.get 6
    local.get 9
    i32.xor
    local.set 10
    local.get 10
    return)
  (func (;5;) (type 0) (param i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32)
    global.get 0
    local.set 1
    i32.const 16
    local.set 2
    local.get 1
    local.get 2
    i32.sub
    local.set 3
    local.get 3
    global.set 0
    local.get 3
    local.get 0
    i32.store offset=12
    local.get 3
    i32.load offset=12
    local.set 4
    local.get 4
    call 2
    local.set 5
    i32.const 1
    local.set 6
    local.get 5
    local.get 6
    i32.and
    local.set 7
    block  ;; label = @1
      local.get 7
      i32.eqz
      br_if 0 (;@1;)
    end
    local.get 3
    i32.load offset=12
    local.set 8
    i32.const 16
    local.set 9
    local.get 8
    local.get 9
    i32.shr_s
    local.set 10
    i32.const 65535
    local.set 11
    local.get 10
    local.get 11
    i32.and
    local.set 12
    i32.const 16
    local.set 13
    local.get 3
    local.get 13
    i32.add
    local.set 14
    local.get 14
    global.set 0
    local.get 12
    return)
  (func (;6;) (type 0) (param i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32)
    global.get 0
    local.set 1
    i32.const 16
    local.set 2
    local.get 1
    local.get 2
    i32.sub
    local.set 3
    local.get 3
    global.set 0
    local.get 3
    local.get 0
    i32.store offset=8
    local.get 3
    i32.load offset=8
    local.set 4
    local.get 4
    call 1
    local.set 5
    i32.const 1
    local.set 6
    local.get 5
    local.get 6
    i32.and
    local.set 7
    block  ;; label = @1
      block  ;; label = @2
        local.get 7
        i32.eqz
        br_if 0 (;@2;)
        local.get 3
        i32.load offset=8
        local.set 8
        i32.const 65535
        local.set 9
        local.get 8
        local.get 9
        i32.and
        local.set 10
        local.get 3
        local.get 10
        i32.store offset=12
        br 1 (;@1;)
      end
      local.get 3
      i32.load offset=8
      local.set 11
      local.get 11
      call 4
      local.set 12
      local.get 3
      local.get 12
      i32.store offset=12
    end
    local.get 3
    i32.load offset=12
    local.set 13
    i32.const 16
    local.set 14
    local.get 3
    local.get 14
    i32.add
    local.set 15
    local.get 15
    global.set 0
    local.get 13
    return)
  (func (;7;) (type 0) (param i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32)
    global.get 0
    local.set 1
    i32.const 16
    local.set 2
    local.get 1
    local.get 2
    i32.sub
    local.set 3
    local.get 3
    local.get 0
    i32.store offset=12
    local.get 3
    i32.load offset=12
    local.set 4
    i32.const -559038737
    local.set 5
    local.get 4
    local.get 5
    i32.mul
    local.set 6
    local.get 3
    i32.load offset=12
    local.set 7
    i32.const -889275714
    local.set 8
    local.get 7
    local.get 8
    i32.add
    local.set 9
    local.get 6
    local.get 9
    i32.xor
    local.set 10
    local.get 10
    return)
  (func (;8;) (type 4) (param i32 i32 i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32)
    global.get 0
    local.set 3
    i32.const 32
    local.set 4
    local.get 3
    local.get 4
    i32.sub
    local.set 5
    local.get 5
    global.set 0
    local.get 5
    local.get 0
    i32.store offset=24
    local.get 5
    local.get 1
    i32.store offset=20
    local.get 5
    local.get 2
    i32.store offset=16
    local.get 5
    i32.load offset=24
    local.set 6
    local.get 5
    i32.load offset=20
    local.set 7
    local.get 6
    local.get 7
    i32.add
    local.set 8
    local.get 8
    call 1
    local.set 9
    i32.const 1
    local.set 10
    local.get 9
    local.get 10
    i32.and
    local.set 11
    block  ;; label = @1
      block  ;; label = @2
        local.get 11
        i32.eqz
        br_if 0 (;@2;)
        local.get 5
        i32.load offset=24
        local.set 12
        local.get 5
        i32.load offset=20
        local.set 13
        local.get 12
        local.get 13
        i32.mul
        local.set 14
        i32.const -559038737
        local.set 15
        local.get 14
        local.get 15
        i32.xor
        local.set 16
        local.get 5
        local.get 16
        i32.store offset=12
        local.get 5
        i32.load offset=16
        local.set 17
        i32.const 3
        local.set 18
        local.get 17
        local.get 18
        i32.shl
        local.set 19
        local.get 5
        i32.load offset=12
        local.set 20
        local.get 20
        local.get 19
        i32.add
        local.set 21
        local.get 5
        local.get 21
        i32.store offset=12
        local.get 5
        i32.load offset=12
        local.set 22
        i32.const -889275714
        local.set 23
        local.get 22
        local.get 23
        i32.xor
        local.set 24
        local.get 5
        local.get 24
        i32.store offset=12
        local.get 5
        i32.load offset=12
        local.set 25
        local.get 5
        local.get 25
        i32.store offset=28
        br 1 (;@1;)
      end
      i32.const 0
      local.set 26
      local.get 5
      local.get 26
      i32.store offset=28
    end
    local.get 5
    i32.load offset=28
    local.set 27
    i32.const 32
    local.set 28
    local.get 5
    local.get 28
    i32.add
    local.set 29
    local.get 29
    global.set 0
    local.get 27
    return)
  (func (;9;) (type 5) (param i32 i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i64 i64 i64)
    global.get 0
    local.set 2
    i32.const 32
    local.set 3
    local.get 2
    local.get 3
    i32.sub
    local.set 4
    local.get 4
    global.set 0
    local.get 4
    local.get 0
    i32.store offset=24
    local.get 4
    local.get 1
    i32.store offset=20
    local.get 4
    i32.load offset=20
    local.set 5
    local.get 5
    call 7
    local.set 6
    local.get 4
    local.get 6
    i32.store offset=16
    local.get 4
    i32.load offset=24
    local.set 7
    i32.const 7777777
    local.set 8
    local.get 7
    local.get 8
    i32.rem_s
    local.set 9
    i32.const 42
    local.set 10
    local.get 9
    local.get 10
    i32.sub
    local.set 11
    local.get 4
    local.get 11
    i32.store offset=12
    local.get 4
    i32.load offset=16
    local.set 12
    i32.const 16711935
    local.set 13
    local.get 12
    local.get 13
    i32.and
    local.set 14
    i32.const 15925324
    local.set 15
    local.get 14
    local.get 15
    i32.xor
    local.set 16
    local.get 4
    local.get 16
    i32.store offset=8
    local.get 4
    i32.load offset=16
    local.set 17
    i32.const 305419896
    local.set 18
    local.get 17
    local.get 18
    i32.xor
    local.set 19
    local.get 19
    local.set 20
    local.get 20
    i64.extend_i32_s
    local.set 46
    i64.const 194484560699266100
    local.set 47
    local.get 46
    local.get 47
    i64.xor
    local.set 48
    local.get 48
    i32.wrap_i64
    local.set 21
    local.get 4
    local.get 21
    i32.store offset=4
    local.get 4
    i32.load offset=12
    local.set 22
    local.get 4
    i32.load offset=8
    local.set 23
    local.get 22
    local.get 23
    i32.or
    local.set 24
    local.get 4
    i32.load offset=4
    local.set 25
    local.get 24
    local.get 25
    i32.or
    local.set 26
    local.get 4
    local.get 26
    i32.store
    local.get 4
    i32.load offset=20
    local.set 27
    local.get 27
    call 2
    local.set 28
    i32.const 1
    local.set 29
    local.get 28
    local.get 29
    i32.and
    local.set 30
    block  ;; label = @1
      block  ;; label = @2
        local.get 30
        i32.eqz
        br_if 0 (;@2;)
        i32.const 0
        local.set 31
        i32.const 1
        local.set 32
        local.get 31
        local.get 32
        i32.and
        local.set 33
        local.get 4
        local.get 33
        i32.store8 offset=31
        br 1 (;@1;)
      end
      local.get 4
      i32.load
      local.set 34
      i32.const 0
      local.set 35
      local.get 34
      local.set 36
      local.get 35
      local.set 37
      local.get 36
      local.get 37
      i32.eq
      local.set 38
      i32.const 1
      local.set 39
      local.get 38
      local.get 39
      i32.and
      local.set 40
      local.get 4
      local.get 40
      i32.store8 offset=31
    end
    local.get 4
    i32.load8_u offset=31
    local.set 41
    i32.const 1
    local.set 42
    local.get 41
    local.get 42
    i32.and
    local.set 43
    i32.const 32
    local.set 44
    local.get 4
    local.get 44
    i32.add
    local.set 45
    local.get 45
    global.set 0
    local.get 43
    return)
  (func (;10;) (type 0) (param i32) (result i32)
    (local i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32 i32)
    global.get 0
    local.set 1
    i32.const 32
    local.set 2
    local.get 1
    local.get 2
    i32.sub
    local.set 3
    local.get 3
    global.set 0
    local.get 3
    local.get 0
    i32.store offset=24
    local.get 3
    i32.load offset=24
    local.set 4
    local.get 4
    call 2
    local.set 5
    i32.const 1
    local.set 6
    local.get 5
    local.get 6
    i32.and
    local.set 7
    block  ;; label = @1
      block  ;; label = @2
        local.get 7
        i32.eqz
        br_if 0 (;@2;)
        i32.const 0
        local.set 8
        i32.const 1
        local.set 9
        local.get 8
        local.get 9
        i32.and
        local.set 10
        local.get 3
        local.get 10
        i32.store8 offset=31
        br 1 (;@1;)
      end
      local.get 3
      i32.load offset=24
      local.set 11
      local.get 11
      call 3
      drop
      local.get 3
      i32.load offset=24
      local.set 12
      local.get 12
      call 4
      drop
      local.get 3
      i32.load offset=24
      local.set 13
      local.get 13
      call 5
      local.set 14
      local.get 3
      local.get 14
      i32.store offset=20
      local.get 3
      i32.load offset=24
      local.set 15
      local.get 15
      call 6
      local.set 16
      local.get 3
      local.get 16
      i32.store offset=16
      local.get 3
      i32.load offset=20
      local.set 17
      local.get 3
      i32.load offset=16
      local.set 18
      local.get 3
      i32.load offset=24
      local.set 19
      local.get 17
      local.get 18
      local.get 19
      call 8
      local.set 20
      local.get 3
      local.get 20
      i32.store offset=12
      local.get 3
      i32.load offset=12
      local.set 21
      local.get 3
      i32.load offset=24
      local.set 22
      local.get 21
      local.get 22
      call 9
      local.set 23
      i32.const 1
      local.set 24
      local.get 23
      local.get 24
      i32.and
      local.set 25
      local.get 3
      local.get 25
      i32.store8 offset=31
    end
    local.get 3
    i32.load8_u offset=31
    local.set 26
    i32.const 1
    local.set 27
    local.get 26
    local.get 27
    i32.and
    local.set 28
    i32.const 32
    local.set 29
    local.get 3
    local.get 29
    i32.add
    local.set 30
    local.get 30
    global.set 0
    local.get 28
    return)
  (func (;11;) (type 1) (result i32)
    global.get 0)
  (func (;12;) (type 3) (param i32)
    local.get 0
    global.set 0)
  (func (;13;) (type 0) (param i32) (result i32)
    (local i32 i32)
    global.get 0
    local.get 0
    i32.sub
    i32.const -16
    i32.and
    local.tee 1
    global.set 0
    local.get 1)
  (func (;14;) (type 2)
    i32.const 5243920
    global.set 2
    i32.const 1040
    i32.const 15
    i32.add
    i32.const -16
    i32.and
    global.set 1)
  (func (;15;) (type 1) (result i32)
    global.get 0
    global.get 1
    i32.sub)
  (func (;16;) (type 1) (result i32)
    global.get 2)
  (func (;17;) (type 1) (result i32)
    global.get 1)
  (func (;18;) (type 3) (param i32))
  (func (;19;) (type 1) (result i32)
    i32.const 1024
    call 18
    i32.const 1028)
  (func (;20;) (type 0) (param i32) (result i32)
    i32.const 1)
  (func (;21;) (type 2)
    (local i32)
    block  ;; label = @1
      call 19
      i32.load
      local.tee 0
      i32.eqz
      br_if 0 (;@1;)
      loop  ;; label = @2
        local.get 0
        call 22
        local.get 0
        i32.load offset=56
        local.tee 0
        br_if 0 (;@2;)
      end
    end
    i32.const 0
    i32.load offset=1032
    call 22
    i32.const 0
    i32.load offset=1032
    call 22
    i32.const 0
    i32.load offset=1032
    call 22)
  (func (;22;) (type 3) (param i32)
    (local i32 i32)
    block  ;; label = @1
      local.get 0
      i32.eqz
      br_if 0 (;@1;)
      block  ;; label = @2
        local.get 0
        i32.load offset=76
        i32.const 0
        i32.lt_s
        br_if 0 (;@2;)
        local.get 0
        call 20
        drop
      end
      block  ;; label = @2
        local.get 0
        i32.load offset=20
        local.get 0
        i32.load offset=28
        i32.eq
        br_if 0 (;@2;)
        local.get 0
        i32.const 0
        i32.const 0
        local.get 0
        i32.load offset=36
        call_indirect (type 4)
        drop
      end
      local.get 0
      i32.load offset=4
      local.tee 1
      local.get 0
      i32.load offset=8
      local.tee 2
      i32.eq
      br_if 0 (;@1;)
      local.get 0
      local.get 1
      local.get 2
      i32.sub
      i64.extend_i32_s
      i32.const 1
      local.get 0
      i32.load offset=40
      call_indirect (type 6)
      drop
    end)
  (func (;23;) (type 1) (result i32)
    i32.const 1036)
  (table (;0;) 1 1 funcref)
  (memory (;0;) 256 256)
  (global (;0;) (mut i32) (i32.const 5243920))
  (global (;1;) (mut i32) (i32.const 0))
  (global (;2;) (mut i32) (i32.const 0))
  (export "memory" (memory 0))
  (export "__wasm_call_ctors" (func 0))
  (export "check_pin" (func 10))
  (export "__indirect_function_table" (table 0))
  (export "__errno_location" (func 23))
  (export "__stdio_exit" (func 21))
  (export "emscripten_stack_init" (func 14))
  (export "emscripten_stack_get_free" (func 15))
  (export "emscripten_stack_get_base" (func 16))
  (export "emscripten_stack_get_end" (func 17))
  (export "stackSave" (func 11))
  (export "stackRestore" (func 12))
  (export "stackAlloc" (func 13)))
