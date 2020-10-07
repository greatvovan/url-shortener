function init_vector(n)
  local vector = {}
  for i = 1,n,1 do
    vector[i] = 0
  end
  return vector
end

function increment_vector(v, base)
  local el
  for i = table.getn(v),1,-1 do
    el = v[i] + 1
    if el == base then
      v[i] = 0
    else
      v[i] = el
      break
    end
  end
end

function map_to_ascii(n)
  if n < 26 then      -- A-Z
    return n + 65     -- [0, 25] --> [65, 90]
  elseif n < 52 then  -- a-z
    return n + 71     -- [26, 51] --> [97, 122]
  elseif n < 62 then  -- 0-9
    return n - 4      -- [52-61] --> [48, 57]
  elseif n < 63 then  -- -
    return 45         -- 62 --> 45
  else                -- ~
    return 126        -- 63 --> 126
  end
end

function vector_to_string(v)
  local ch = {}
  for i = 1,table.getn(v),1 do
    ch[i] = string.char(map_to_ascii(v[i]))
  end
  return table.concat(ch, "")
end

function generate_keys(space, len)
  local base = 64     -- Another (greater) base will require vector_to_string() modification.
  local total_num = base^len
  local vector = init_vector(len)
  local key
  local space = box.space[space]
  box.session.push('Generating '..total_num..' keys')
  for i = 1,total_num,1 do
    key = vector_to_string(vector)
    space:insert({key})
    increment_vector(vector, base)
    if i % 100000 == 0 then
      box.session.push(string.format('%d done', i))
    end
  end

  box.session.push('Generation completed')
end

function init_storage(key_len)
  local keys = box.space.keys
  local urls = box.space.urls

  if keys ~= nil then
    keys:drop()
  end
  keys = box.schema.create_space('keys')
  keys:format({{name = 'id', type = 'string'}})
  keys:create_index('primary', {type = 'hash', parts = {'id'}})
  box.session.push('"keys" space created')

  if urls ~= nil then
    urls:drop()
  end
  urls = box.schema.create_space('urls')
  urls:format({
    {name = 'id', type = 'string' },
    {name = 'url', type = 'string' },
    {name = 'create_ts', type = 'integer' },
    {name = 'expiry_ts', type = 'integer' }
    })
  urls:create_index('primary', {type = 'hash', parts = {'id'}})
  box.session.push('"urls" space created')

  generate_keys('keys', key_len)
  box.session.push('Storage initialization completed')
end
