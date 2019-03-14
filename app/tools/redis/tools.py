# -*- coding: UTF-8 -*-
"""
@author: ycx
@date: 2018/10/19 
"""
import redis
import inspect
import pickle
from app import config


class RedisCached(object):
    def __init__(self, rc=None):
        self.rc = rc

    def _gen_key(self, pattern, names, args):
        values = args[:len(names)]
        replaces = dict(zip(names, values))
        return pattern.format(**replaces)

    def set(self, pattern, timeout=0):
        """
        redis缓存包装器
        :param pattern: 缓存模式 `rc:video:{video_id}`
        :param timeout: 超时时间
        """

        def decorator(f):
            def run(*args, **kwargs):
                argspec = inspect.getargspec(f)
                if argspec.varargs or argspec.keywords:
                    raise Exception("not support args or kwargs")
                name = self._gen_key(pattern, argspec.args, args)
                response = self.rc.get(name)
                if response is None:
                    response = f(*args, **kwargs)
                    self.rc.set(name, pickle.dumps(response))
                    if timeout:
                        self.rc.expire(name, timeout)
                else:
                    response = pickle.loads(response)
                return response

            return run

        return decorator

    def delete(self, pattern):
        def decorator(f):
            def run(*args, **kwargs):
                argspec = inspect.getargspec(f)
                if argspec.varargs or argspec.keywords:
                    raise Exception("not support args or kwargs")
                name = self._gen_key(pattern, argspec.args, args)
                response = f(*args, **kwargs)
                if response:
                    redis.delete(name)
                return response

            return run

        return decorator


# 改为阿里云-crm-20180713
class RedisCachedYun(object):
    def __init__(self):
        try:
            self.rc = redis.StrictRedis.from_url(config.REDIS_URL)
        except Exception as e:
            print("连接redis失败", e)
        else:
            print('连接redis成功')

    def get(self, key):
        return self.rc.get(key)

    def set_key(self, key, value):
        return self.rc.set(key, value)

    def delete_key(self, key):
        return self.rc.delete(key)

    def _gen_key(self, pattern, names, args):
        values = args[:len(names)]
        replaces = dict(zip(names, values))
        return pattern.format(**replaces)

    # def set(self, key, value):
    #     return self.rc.set(key, value)
    def expire(self, key, time):
        return self.rc.expire(key, time)

    def hget(self, key, subkey):
        return self.rc.hget(key, subkey)

    def hset(self, key, subkey, value):
        return self.rc.hset(key, subkey, value)

    def hgetall(self, key):
        return self.rc.hgetall(key)

    def hmset(self, key, value):
        return self.rc.hmset(key, value)

    def rpush(self, key, value):
        return self.rc.rpush(key, value)

    def redis_lrange(self, key):
        return self.rc.lrange(key, 0, -1)

    def llen(self, key):
        return self.rc.llen(key)  # 返回队列里面list内元素的数量

    def get_nowait(self, key):
        # 直接返回队列第一个元素，如果队列为空返回的是None
        item = self.rc.lpop(key)
        return item

    def rpop(self, key):
        return self.rc.rpop(key)

    def set(self, pattern, timeout=0):
        """
        redis缓存包装器

        :param pattern: 缓存模式 `rc:video:{video_id}`
        :param timeout: 超时时间
        """

        def decorator(f):
            def run(*args, **kwargs):
                argspec = inspect.getargspec(f)
                if argspec.varargs or argspec.keywords:
                    raise Exception("not support args or kwargs")
                name = self._gen_key(pattern, argspec.args, args)
                response = self.rc.get(name)
                if response is None:
                    response = f(*args, **kwargs)
                    self.rc.set(name, pickle.dumps(response))
                    if timeout:
                        self.rc.expire(name, timeout)
                else:
                    response = pickle.loads(response)
                return response

            return run

        return decorator

    def delete(self, pattern):
        def decorator(f):
            def run(*args, **kwargs):
                argspec = inspect.getargspec(f)
                if argspec.varargs or argspec.keywords:
                    raise Exception("not support args or kwargs")
                name = self._gen_key(pattern, argspec.args, args)
                response = f(*args, **kwargs)
                if response:
                    self.rc.delete(name)
                return response

            return run

        return decorator

    def lpush(self, key, value):
        return self.rc.lpush(key, value)

    def sismember(self, key, value):
        return self.rc.sismember(key, value)

    def sadd(self, key, value):
        return self.rc.sadd(key, value)

    def srem(self, key, value):
        return self.rc.srem(key, value)

    def smembers(self, key):
        return self.rc.smembers(key)


rc_yun = RedisCachedYun()
