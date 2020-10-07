function store_url(url, created_ts, expiry_ts, rnd_seed)
    local key
    box.begin()
    key = box.space.keys.index.primary:random(rnd_seed)[1]
    box.space.keys:delete{key}
    box.space.urls:insert{key, url, created_ts, expiry_ts }
    box.commit()
    return key
end
