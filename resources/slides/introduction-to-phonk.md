---
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff
marp: true
---

<style>
section::after {
  font-weight: bold;
  font-size: 0.6em;
  text-shadow: 1px 1px 0 #fff;
  content: 'Page ' attr(data-marpit-pagination);
}
</style>

# **Introduction to Phonk**

by f4r4w4y

---

# Personal Preface

My name is Muhammad Fakhri "f4r4w4y" Putra Supriyadi.

Im a software engineer that create and (occasionaly) break some software, i also have some obsession to electronics and robotics.

```
You can reach me here:

- f4r4w4y#6907 [discord]
- @0xfa1 [twitter]
- fakhriputra123s [gmail]
```

---

# What is Phonk

Generally, phonk is just a scripting tools for android based apps that can be used for so many purposes.

In fact, lots of stuff including some that related to IoT can also be created using phonk without needing any knowledge regarding android development itself.

`Phonk == Python for android`, so to speak.

---

# Who's behind Phonk

[Víctor Díaz Barrales](http://victordiazbarrales.com/) a person that have done so many awesome projects with his team including [City Fireflies](http://victordiazbarrales.com/projects/city-fireflies).

He is the main contributor and the creator of Phonk, a project that he already been working since 2013 (based on his [website](http://victordiazbarrales.com/projects/phonk)).

---

# What can we do with Phonk

Simple answer is **SO MANY**, as to the fact that this is a general scripting tools for android based apps, we can create almost anything using this toolbox.

As you can see on this [reference documentation](https://phonk.app/docs/reference), there are so many stuff we can do using Phonk.

We can even connect to some IoT Protocol such as MQTT, HTTP(S), BLE, Websockets and more.

---

# What's happening under the hood

Phonk uses [Rhino](https://github.com/mozilla/rhino) which is a JavaScript implementation fully written in Java so that we can use it in any devices running Java like android for example.

By using Rhino and integrate it with so many on-device sensors and other library in android, Phonk are able to create so many APIs that we can use in a lot easier fashion using JavaScript. 

---

# 