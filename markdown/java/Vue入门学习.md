# 模板语法


模板语法分为：插值语法、指令语法


插值语法使用 {{}}


指令语法 v-bind


```
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <script src="../js/vue.js"></script>
</head>

<body>
<div id="root">
    <p>我的名字：{{name}}</p>
    <a v-bind:href="url">百度一下</a>
</div>

<Script>
    Vue.config.productionTip = false;
    new Vue({
        el: '#root',
        data: {
            name: '青橙',
            url: 'https://www.baidu.com'
        }
    })
</Script>
</body>

</html>
```


# 数据绑定


单项数据绑定 (v-bind)：数据只能从data流向页面。


> v-bind 可以简写为  ：



双向数据绑定（v-model）：数据可以从data流向页面，也可以从页面流向data。


> v-model只能作用在表单元素上。v-model:vue可以简写成 v-model，因为v-model默认收集的就是value的值。



```
<body>
    <div id="root">
        单向数据绑定：<input type="text" v-bind:value="name" />{{name}}


        双向数据绑定：<input type="text" v-model:value="age" />{{age}}
    </div>
    <script>
        new Vue({
            el: '#root',
            data: {
                name: '青橙',
                age: 25
            }
        });

    </script>
</body>
```


# el和data的两种写法


el 的第一种写法


```
<body>
    <div id="root">

    </div>
    <script>
        new Vue({
            el:'#root',
            data:{

            }
        });
    </script>
</body>
```


el 的第二种写法


```
<body>
    <div id="root">

    </div>
    <script>
        const v = new Vue({
            data: {
                name: 'hello'
            }
        });

        v.$mount('#root');
    </script>
</body>
```


data 的第一种写法: 对象式


```
<script>
    const v = new Vue({
        el:'#root',
        data: {
            name: 'hello'
        }
    });
</script>
```


data 的第二种写法: 函数式


```
<script>
    const v = new Vue({
        el: '#root',
        data() {
            return {
                name: 'hello'
            }
        }
    });
</script>
```


# 事件处理


## v-on


> 点击显示信息
>
> 或
>
> <button @click="showInfo()">点击显示信息



```
<body>
    <div id='root'>
        <button v-on:click="showInfo()">点击显示信息</button>
    </div>
    <script>
        new Vue({
            el: '#root',
            data() {
                return {
                    name: '青橙'
                }
            },
            methods: {
                showInfo() {
                    alert('hello,' + this.name)
                }
            }
        })
    </script>
</body>
```


## 事件修饰符


vue中的事件修饰符


1. prevent：阻止默认事件
2. stop：阻止事件冒泡
3. once：事件只触发一次
4. capture：使用事件的捕获模式
5. self：只有event.target是当前操作的元素才触发事件
6. passive：事件的默认行为立即执行，无需等待事件回调执行完毕



```
<body>
    <div id="root">
        <!-- a标签的默认行为被阻止 -->
        <a href="http://www.baidu.com" v-on:click.prvent='showInfo'>点击我</a>
    </div>
    <script>
        Vue.config.productionTip = false;
        new Vue({
            el: '#root',
            data() {
                return {

                }
            },
            methods: {
                showInfo() {
                    alert('hello....')
                }
            }
        })
    </script>
</body>
```


## 键盘事件


keyup 和 keydown的区别：


keyup：按键弹起时被触发。keydown：按键被按下的时候被触发。


vue中常用的按键别名


- 回车：enter
- 删除：delete
- 退出：esc
- 空格：space
- 换行：tab
- 上：up
- 下：down
- 左：left
- 右：right



```
<body>
    <div id="root">
        <!-- 输入之后按回车键触发 控制台输出value值-->
        <input type="text" v-on:keyup.enter='showInfo' />
    </div>
    <script>
        Vue.config.productionTip = false;
        new Vue({
            el: '#root',
            data() {
                return {

                }
            },
            methods: {
                showInfo(e) {
                    console.log(e.target.value);
                }
            }
        })
    </script>
</body>
```


# 计算属性-computed


计算属性和方法的区别：计算属性的结果会被缓存，只有当依赖的属性发生改变时会被调用。


```
<body>
    <div id="root">
        <input type="text" v-model="fristname">

        <input type="text" v-model="lastname">

        全名：{{fullname}}
    </div>
    <script>
        new Vue({
            el: '#root',
            data: {
                fristname: '张',
                lastname: '三'
            },
            computed: {
                fullname: {
                    get() {
                        return this.fristname + '-' + this.lastname
                    }
                }
            }
        })
    </script>
</body>
```


完整形式,， 当要修改计算属性时，计算属性要加上 set()


```
computed: {
    fullname: {
        get() {
            return this.fristname + '-' + this.lastname
        },
        set(value){

        }
    }
}
```


简写形式，没有 set()，默认就是get()


```
computed: {
    fullname() {
        return this.fristname + '-' + this.lastname
    }
}
```


# 侦听器-watch


监听某一个属性的变化， 当监听的属性变化时被调用。


```
<body>
    <div id="root">
        <h3>今天心情很好！</h3>
        <button @click='changeMood'>改变心情</button>
    </div>
    <script>
        new Vue({
            el: '#root',
            data: {
                isGood: true
            },
            methods: {
                changeMood() {
                    console.log("执行changeMood");
                    this.isGood = !this.isGood;
                }
            },
            watch:{
                isGood:{

                    handler(newValue,oldValue){
                        console.log('isGood的值改变了,改变前：',oldValue,'，改变后',newValue);
                    }
                }
            }
        })
    </script>
</body>
```


watch完整写法


```
    vm.$watch('isGood', {
        immediate: true, //初始化的时候调用handler
        deep: true, //深度监听，比如说对象中的属性改变
        handler(newValue, oldValue) {
            console.log('isGood的值改变了,改变前：', oldValue, '，改变后', newValue);
        }
    });
```


watch简写


```
vm.$watch('isGood', function (newValue, oldValue) {
    console.log('isGood的值改变了,改变前：', oldValue, '，改变后', newValue)
});
```


**computed 和 watch 的区别**


computed可以计算多个属性， 依赖的某一个属性发生改变时就会被调用，而watch只能监听一个属性。


watch可以做异步操作，computed不可以。


# 绑定样式


## 绑定 HTML Class


在将 `v-bind` 用于 `class` 和 `style` 时，Vue.js 做了专门的增强。表达式结果的类型除了字符串之外，还可以是对象或数组


### 对象语法


可以传给 `v-bind:class` 一个对象，以动态地切换 class：


```
<div v-bind:class="{ active: isActive , happy:isHappy }"></div>
```


data：


```
data: {
  isMood: true,
  isHappy: true
}
```


绑定的数据对象不必内联定义在模板里：


```
<div v-bind:class="classObject"></div>
data: {
  classObject: {
    active: true,
    'text-danger': false
  }
}
```


绑定一个返回对象的计算属性。这是一个常用且强大的模式：


```
<div v-bind:class="classObject"></div>
data: {
  isActive: true,
  error: null
},
computed: {
  classObject: function () {
    return {
      active: this.isActive && !this.error,
      'text-danger': this.error && this.error.type === 'fatal'
    }
  }
}
```


### 数组语法


可以把一个数组传给 `v-bind:class`，以应用一个 class 列表：


```
<div v-bind:class="[activeClass, errorClass]"></div>
data: {
  activeClass: 'active',
  errorClass: 'text-danger'
}
```


渲染为：


```
<div class="active text-danger"></div>
```


# 条件渲染


```
<h1 v-if="awesome">Vue is awesome!</h1>
<h1 v-else>Oh no 😢</h1>
```


data


```
data:{
    awesome: true
}
```


# 列表渲染


我们可以用 `v-for` 指令基于一个数组来渲染一个列表。`v-for` 指令需要使用 `item in items` 形式的特殊语法，其中 `items` 是源数据数组，而 `item` 则是被迭代的数组元素的**别名**。


```
<ul id="example-1">
  <li v-for="item in items" :key="item.message">
    {{ item.message }}
  </li>
</ul>
var example1 = new Vue({
  el: '#example-1',
  data: {
    items: [
      { message: 'Foo' },
      { message: 'Bar' }
    ]
  }
})
```


结果：


- Foo
- Bar



在 `v-for` 块中，我们可以访问所有父作用域的 property。`v-for` 还支持一个可选的第二个参数，即当前项的索引。


```
<ul id="example-2">
  <li v-for="(item, index) in items">
    {{ parentMessage }} - {{ index }} - {{ item.message }}
  </li>
</ul>
var example2 = new Vue({
  el: '#example-2',
  data: {
    parentMessage: 'Parent',
    items: [
      { message: 'Foo' },
      { message: 'Bar' }
    ]
  }
})
```


结果：


- Parent - 0 - Foo
- Parent - 1 - Bar



# 过滤器


Vue.js 允许你自定义过滤器，可被用于一些常见的文本格式化。过滤器可以用在两个地方：**双花括号插值和 **`**v-bind**`** 表达式** (后者从 2.1.0+ 开始支持)。过滤器应该被添加在 JavaScript 表达式的尾部，由“管道”符号指示：


```
<!-- 在双花括号中 -->
{{ message | capitalize }}
<!-- 在 `v-bind` 中 -->
<div v-bind:id="rawId | formatId"></div>
```


你可以在一个组件的选项中定义本地的过滤器：


```
filters: {
  capitalize: function (value) {
    if (!value) return ''
    value = value.toString()
    return value.charAt(0).toUpperCase() + value.slice(1)
  }
}
```


或者在创建 Vue 实例之前全局定义过滤器：


```
Vue.filter('capitalize', function (value) {
  if (!value) return ''
  value = value.toString()
  return value.charAt(0).toUpperCase() + value.slice(1)
})
new Vue({
  // ...
})
```


当全局过滤器和局部过滤器重名时，会采用局部过滤器。


# 组件基础


```
<body>
    <div id="root">
        <student></student>
    </div>
    <script>
        Vue.config.productionTip = false

        const student = Vue.extend({
            data() {
                return {
                    name: 'orange',
                    age: 25,
                    gender: '男'
                }
            },
            template: `
            <div>
                姓名：{{ name }}
                年龄：{{ age }}
                性别：{{ gender }}
            </div>
                 `
        })

        new Vue({
            el: '#root',
            components: {
                student
            }
        })
    </script>
</body>
```


# vuecli 脚手架


Vue CLI 是一个基于 Vue.js 进行快速开发的完整系统


- 基于 webpack 构建，并带有合理的默认配置；
- 可以通过项目内的配置文件进行配置；
- 可以通过插件进行扩展。



运行以下命令来创建一个新项目：


```
vue create hello-world
```


## vue.config.js


`vue.config.js` 是一个可选的配置文件，如果项目的 (和 `package.json` 同级的) 根目录中存在这个文件，那么它会被 `@vue/cli-service` 自动加载。


```
// vue.config.js

/**
 * @type {import('@vue/cli-service').ProjectOptions}
 */
module.exports = {
  // 选项...
}
```


# ref


`ref` 被用来给元素或子组件注册引用信息。引用信息将会注册在父组件的 `$refs` 对象上。如果在普通的 DOM 元素上使用，引用指向的就是 DOM 元素；如果用在子组件上，引用就指向组件实例


标识


```
<p ref="p">{{msg}}</p>
```


获取


```
this.$refs.p
```


# props


props 可以是数组或对象，用于接收来自父组件的数据。props 可以是简单的数组，或者使用对象作为替代，对象允许配置高级选项，如类型检测、自定义验证和设置默认值。


- **示例**：



```
// 简单语法
Vue.component('props-demo-simple', {
  props: ['size', 'myMessage']
})
// 对象语法，提供验证
Vue.component('props-demo-advanced', {
  props: {
    // 检测类型
    height: Number,
    // 检测类型 + 其他验证
    age: {
      type: Number,
      default: 0,
      required: true,
      validator: function (value) {
        return value >= 0
      }
    }
  }
})
```


## 父向子组件传值


父组件向子组件传值用**属性传值**


父组件


```
<template>
  <div id="app">
    <HelloWorld :msg="message" />
  </div>
</template>

<script>
import HelloWorld from "./components/HelloWorld.vue";

export default {
  name: "App",
  components: {
    HelloWorld,
  },
  data() {
    return {
      message: "今天天气不错"
    };
  },
};
</script>
```


子组件


```
<template>
  <div class="hello">
    <p>父组件传过来的值：{{ msg }}</p>
  </div>
</template>

<script>
export default {
  name: "HelloWorld",
  props: {
    msg: String,
  },
};
</script>
```


## 子向父组件传值


子组件向父组件传值用**函数传值**


父组件


```
<template>
  <div id="app">
    <HelloWorld :receive="receive" />
    <p>子组件传过来的值：{{message}}</p>
  </div>
</template>

<script>
import HelloWorld from "./components/HelloWorld.vue";

export default {
  name: "App",
  components: {
    HelloWorld,
  },
  data() {
    return {
      message: "",
    };
  },
  methods: {
    receive(value) {
      this.message = value;
    },
  },
};
</script>
```


子组件


```
<template>
  <div class="hello">
    <input type="text" v-model="message" />
    <input type="button" value="传值" @click="add" />
  </div>
</template>

<script>
export default {
  name: "HelloWorld",
  props: ["receive"],
  data() {
    return {
      message: "",
    };
  },
  methods: {
    add() {
      this.receive(this.message);
    },
  },
};
</script>
```


# 自定义事件


不同于组件和 prop，事件名不存在任何自动化的大小写转换。而是触发的事件名需要完全匹配监听这个事件所用的名称。举个例子，如果触发一个 camelCase 名字的事件：


```
this.$emit('myEvent')
```


则监听这个名字的 kebab-case 版本是不会有任何效果的：


```
<!-- 没有效果 -->
<my-component v-on:my-event="doSomething"></my-component>
```


不同于组件和 prop，事件名不会被用作一个 JavaScript 变量名或 property 名，所以就没有理由使用 camelCase 或 PascalCase 了。并且 `v-on` 事件监听器在 DOM 模板中会被自动转换为全小写 (因为 HTML 是大小写不敏感的)，所以 `v-on:myEvent` 将会变成 `v-on:myevent`——导致 `myEvent` 不可能被监听到。


因此，我们推荐你**始终使用 kebab-case 的事件名**。


自定义事件实现子组件向父组件传值


父组件


```
<template>
  <div id="app">
    <HelloWorld v-on:my-event="receive" />
    <p>子组件传过来的值：{{ message }}</p>
  </div>
</template>

<script>
import HelloWorld from "./components/HelloWorld.vue";

export default {
  name: "App",
  components: {
    HelloWorld,
  },
  data() {
    return {
      message: "",
    };
  },
  methods: {
    receive(value) {
      this.message = value;
    },
  },
};
</script>
```


子组件


```
<template>
  <div class="hello">
    <input type="text" v-model="message" />
    <input type="button" value="传值" @click="add" />
  </div>
</template>

<script>
export default {
  name: "HelloWorld",
  data() {
    return {
      message: "",
    };
  },
  methods: {
    add() {
      this.$emit("my-event", this.message);
    },
  },
};
</script>
```


# 全局事件总线


一种适用于任意间组件传值的方式


使用方式


注册全局事件总线


```
import Vue from 'vue'
import App from './App.vue'

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
  beforeCreate() {
    Vue.prototype.$bus = this //注册全局事件总线
  }
}).$mount('#app')
```


接收数据


```
mounted() {
  this.$bus.$on("hello", (data) => {
    this.orangeMessage = data;
  });
}
```


发送数据


```
 methods: {
    send() {
      this.$bus.$emit("hello", this.message);
    },
  },
```


# axios


使用axios发送请求


安装 axios


```
npm install axios
```


使用


```
import axios from "axios";
export default {
  name: "User",
  methods: {
    getUser() {
      axios
        .get("https://localhost:8080/api/user/getuser")
        .then((res) => {
          console.log("res", res);
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
  },
};
```


# 配置代理


如果你的前端应用和后端 API 服务器没有运行在同一个主机上，你需要在开发环境下将 API 请求代理到 API 服务器。这个问题可以通过 `vue.config.js` 中的 `devServer.proxy` 选项来配置。


```
module.exports = {
    devServer: {
        proxy: {
            '/api': {
                target: 'http://localhost:80',
                pathRewrite: { '^/api': '' },//将以 /api 开头的请求转发到http://localhost:80, 但请求时去掉/api
                ws: true, //用于支持webSocket
                changeOrigin: true //用于控制请求头中的host值
            },
            '/foo': {
                target: '<other_url>'
            }
        }
    }
}
```


# 插槽 slot


## 默认插槽


它允许你像这样合成组件：


```
<navigation-link url="/profile">
  Your Profile
</navigation-link>
```


然后你在 `<navigation-link>` 的模板中可能会写为：


```
<a v-bind:href="url" class="nav-link"
>
  <slot></slot>
</a>
```


当组件渲染的时候，`<slot></slot>` 将会被替换为“Your Profile”。插槽内可以包含任何模板代码，包括 HTML：


```
<navigation-link url="/profile">
  <!-- 添加一个 Font Awesome 图标 -->
  <span class="fa fa-user"></span>
  Your Profile
</navigation-link>
```


甚至其它的组件：


```
<navigation-link url="/profile">
  <!-- 添加一个图标的组件 -->
  <font-awesome-icon name="user"></font-awesome-icon>
  Your Profile
</navigation-link>
```


> 注意：如果 `<navigation-link>` 的 `template` 中**没有**包含一个 `<slot>` 元素，则该组件起始标签和结束标签之间的任何内容都会被抛弃。



## 有名字的插槽


```
<template>
  <div id="app">
    <HelloWorld>
      <div slot="center" class="slotcenter">
        <p>这是组件插槽的内容</p>
      </div>
    </HelloWorld>
  </div>
</template>
```


然后在 `<HelloWorld>`中这样写


```
<template>
  <div id="app">
    <HelloWorld>
      <div slot="center" class="slotcenter">
        <p>这是组件插槽的内容</p>
      </div>
    </HelloWorld>
  </div>
</template>
```


# Vuex


Vuex 是一个专为 Vue.js 应用程序开发的**状态管理模式**。它采用集中式存储管理应用的所有组件的状态，并以相应的规则保证状态以一种可预测的方式发生变化。


## 简单使用


安装Vuex


```
npm install vuex
```


创建Vuex ：src/store/index.js


```
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)
//准备actions 用于相应组件中的动作
const actions = {
    jia(context, value) {
        context.commit('JIA', value)
    }
}
//准备mutations 用于操作数据（state）
const mutations = {
    JIA(state, value) {
        state.sum += value
    }
}
//准备state 用于存储数据
const state = {
    sum: 0
}

const store = new Vuex.Store({
    actions,
    mutations,
    state

})
export default store
```


main.js 引入store


```
import Vue from 'vue'
import App from './App.vue'
import store from './store'

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
  store
}).$mount('#app')
```


使用


```
<template>
  <div class="hello">
    <p>结果为：{{ $store.state.sum }}</p>
    <input type="button" value="点击加一" @click="increment" />
  </div>
</template>

<script>
export default {
  name: "hello",
  data() {
    return {
      number: 1,
    };
  },
  methods: {
    increment() {
      this.$store.dispatch("jia", this.number);
    },
  },
};
</script>
```


## getters


getters是对state 的数据进行操作，包装


```
const getters = {
    bigSum(state) {
        return state.sum * 10
    }
}

const store = new Vuex.Store({
    actions,
    mutations,
    state,
    getters

})
```


获取


```
 computed: {
    getbigSum() {
      return this.$store.getters.bigSum;
    },
  }
```


## mapState


mapState用于获取state中的数据


在不用mapState之前这样获取数据


```
<template>
  <div class="hello">
    <p>姓名：{{ name }}</p>
    <p>年龄：{{ age }}</p>
    <p>性别：{{ gender }}</p>
  </div>
</template>

<script>
export default {
  name: "hello",
  computed: {
    name() {
      return this.$store.state.name;
    },
    age() {
      return this.$store.state.age;
    },
    gender() {
      return this.$store.state.gender;
    },
  },
};
</script>
```


使用mapState，这样取值


```
<template>
  <div class="hello">
    <p>姓名：{{ name }}</p>
    <p>年龄：{{ age }}</p>
    <p>性别：{{ gender }}</p>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "hello",
  computed: {
    //第一种写法，对象写法
    // ...mapState({ name: "name", age: "age", gender: "gender" }),

    //第二种写法，数组写法
    ...mapState(["name", "age", "gender"]),
  },
};
</script>
```


## mapGetters


mapGetters和mapState的用法一样


## 模块化


将 actions、mutations、state 模块化


```
import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

//用户相关
const userOptions = {
    namespaced: true,
    actions: {
        addUser(context, value) {
            console.log("执行addUSer", value);
            context.commit('ADD_USER', value)
        }
    },
    mutations: {
        ADD_USER(state, value) {
            state.users.unshift(value)
        }
    },
    state: {
        users: [
            { name: 'orange', age: 25, gender: '男' },
            { name: 'lemon', age: 23, gender: '男' }
        ]
    }
}


const store = new Vuex.Store({
    modules: {
        userAbout: userOptions
    }
})
export default store
```


获取数据和操作数据


```
<template>
  <div class="hello">
    <form>
      <label for="user.name">用户名</label>
      <input type="text" v-model="user.name" />


      <label for="user.age">年龄</label>
      <input type="text" v-model.number="user.age" />


      <input type="radio" id="one" value="男" v-model="user.gender" />
      <label for="one">男</label>
      <input type="radio" id="two" value="女" v-model="user.gender" />
      <label for="two">女</label>


      <input type="button" @click="insertUser" value="添加用户" />
    </form>
    <ul>
      <li v-for="(u, index) in users" :key="index">
        {{ u.name }}-{{ u.age }}-{{ u.gender }}
      </li>
    </ul>
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  name: "hello",
  data() {
    return {
      user: {
        gender: "男",
      },
    };
  },
  computed: {
    ...mapState("userAbout", ["users"]),
  },
  methods: {
    insertUser() {
      this.$store.dispatch("userAbout/addUser", this.user);
    },
  },
};
</script>
```


# Vue Router


## 基本使用


安装路由


```bash
npm install vue-router
```


创建路由 `src/router/index.js`


```javascript
import Vue from 'vue'
import Router from 'vue-router'

import Home from "../components/Home.vue"
import About from "../components/About.vue"

Vue.use(Router)

const router = new Router({
    routes: [
        {
            path: '/home',
            component: Home
        },
        {
            path: '/about',
            component: About
        }
    ]
})

export default router
```


在`main.js`中


```javascript
import Vue from 'vue'
import App from './App.vue'
import router from './router'


Vue.config.productionTip = false

new Vue({
  render: h => h(App),
  router
}).$mount('#app')
```


在组件中使用

```
<template>
  <div id="app">
    <div class="routeBox">
      <ul class="navbar-nav">
        <li class="nav-item">
          <router-link class="nav-link" active-class="active" to="/home">Home</router-link>
        </li>
        <li class="nav-item">
          <router-link class="nav-link" active-class="active" to="/about">About</router-link>
        </li>
      </ul>
    </div>
    <div class="contentBox">
      <router-view></router-view>
    </div>
  </div>
</template>
```


## 多级路由


二级路由不需要以 '/' 开头


```javascript
import Vue from 'vue'
import Router from 'vue-router'

import Home from "../components/Home.vue"
import About from "../components/About.vue"

import News from "../components/News.vue"
import Message from "../components/Message.vue"

Vue.use(Router)

const router = new Router({
    routes: [
        {
            path: '/home',
            component: Home,
            children: [
                {
                    path: 'news',
                    component: News
                },
                {
                    path:'message',
                    component:Message
                }

            ]
        },
        {
            path: '/about',
            component: About
        }
    ]
})

export default router
```


## 路由query参数


路由传参的两种写法


```
<!-- 第一种写法，字符窜写法 -->
<router-link active-class="active" :to="`/home?id=${user.id}&name=${user.name}`" >Home</router-link>


<!-- 第二种写法，对象写法 -->
<router-link active-class="active" :to="{
      path: '/home',
      query: {
        id: user.id,
        name: user.name,
      },
	}"
>Home</router-link
```


获取参数


```
<template>
  <div class=".container">
    <p>获取到路由参数id: {{ $route.query.id }}</p>
    <p>获取到路由参数name: {{ $route.query.name }}</p>
  </div>
</template>
```


## 命名路由


创建路由的时候加上`name`属性，跳转的时候指定`name`名称就行


```javascript
const router = new Router({
    routes: [
        {
            name:'myhome',
            path: '/home',
            component: Home,
        }
    ]
})

export default router ``` 跳转 ``` <router-link:to="{ name: 'myhome' }">Home</router-link >

<--!配合传参-->
<router-link :to="{
  name: 'myhome',
  query: {
    id: user.id,
    name: user.name,
  },
}">Home</router-link>
```


## 路由params参数


传递params参数需要在路由上写明


```javascript
const router = new Router({
    routes: [
        {
            name:'myhome',
            path: '/home/:id/:name',
            component: Home,
        }
    ]
})

export default router
```


跳转时放入参数


```
<--! 方式一 -->
<router-link :to="`/home/${user.id}/${user.name}`">Home</router-link>

<--! 方式二  注意：这里不能使用 path ，只能使用name -->
<router-link :to="{
  name: 'myhome',
  params: {
    id: user.id,
    name: user.name,
  },
}">Home</router-link>
```


接收参数


```
<template>
  <div class=".container">
    <p>获取到路由参数id: {{ $route.params.id }}</p>
    <p>获取到路由参数name: {{ $route.params.name }}</p>
  </div>
</template>
```


## `<router-link>`的replace属性


在`<router-link>`标签中加上**replace**属性后不可后退 ，默认时push，可回退。


```
<router-link :replace="true" to="/home"></router-link>

<!--简写模式 -->
<router-link replace to="home"></router-link>
```


## 编程式路由导航


**push**和**replace**的区别：push可回退，replace不可回退


```javascript

methods: {
    toAbout() {
      this.$router.push("/about");
    },
  },

//传递参数
methods: {
    toAbout() {
      this.$router.push({
        name: "toabout",
        params: {
          id: 1,
          name: "orange",
        },
      });
    },
```


back：后退，forward：前进，to：去第几步


```javascript
this.$router.back()

this.$router.forward()

this.$router.go(number)
```


## 缓存路由组件


让不展示的路由组件保持挂载，不被销毁。


比如说有一个路由组件是表单输入，输入类容后切换走在切换回来时，输入的内容还在


属性 include 是组件的名字, 可以是一个数组


```
<keep-alive include="Form">
	<router-view></router-view>
</keep-alive>


<keep-alive include="['Form','Home']">
	<router-view></router-view>
</keep-alive>
```


## 路由生命周期钩子


用于捕获路由的激活状态的两个生命周期钩子函数


```javascript
//路由组件被激活
activated() {},

// 路由组件失活
deactivated() {},
```


## 全局路由守卫


**全局前置路由守卫:** 在初始化 和 切换路由前调用


可以用来做登录校验 ， 权限校验


```javascript
import Vue from 'vue'
import Router from 'vue-router'

import Home from "../components/Home.vue"
import About from "../components/About.vue"

Vue.use(Router)

const router = new Router({
    routes: [
        {
            name: 'myhome',
            path: '/home',
            component: Home,
        },
        {
            name: 'toabout',
            path: '/about',
            component: About
        }
    ]
})


//to:去什么位置;
//from:当前位置;
//next:放行
router.beforeEach((to, from, next) => {
    console.log('beforeEach', to);
    if (to.path === '/home') {
        //判断是否登录
    } else {
        //放行
        next()
    }
})

export default router
```


如果有很多路由都需要认证， 可以在创建路由的时候加上**meta**属性并且写上标识来判断是否需要认证


```javascript
import Vue from 'vue'
import Router from 'vue-router'

import Home from "../components/Home.vue"
import About from "../components/About.vue"

Vue.use(Router)

const router = new Router({
    routes: [
        {
            name: 'myhome',
            path: '/home',
            component: Home,
            meta: { isAuth: true }
        },
        {
            name: 'toabout',
            path: '/about',
            component: About
        }
    ]
})

// 全局前置路由守卫: 在初始化 和 切换路由前调用

//to:去什么位置; from:当前位置; next:放行
router.beforeEach((to, from, next) => {
    if (to.meta.isAuth) {
        //判断是否登录
        console.log('需要登录');
    } else {
        //放行
        next()
    }
})

export default router
```


**全局后置路由守卫:** 在初始化 和 切换路由之后调用


```javascript
router.afterEach((to, from) => {

})
```


## 独享路由守卫


独享路由守卫只有前置守卫，没有后置守卫。


```javascript
import Vue from 'vue'
import Router from 'vue-router'

import Home from "../components/Home.vue"
import About from "../components/About.vue"

Vue.use(Router)

const router = new Router({
    routes: [
        {
            name: 'myhome',
            path: '/home',
            component: Home,
            meta: { isAuth: true },
            beforeEnter: (to, from, next) => {

            }

        },
        {
            name: 'toabout',
            path: '/about',
            component: About
        }
    ]
})

export default router
```


## 路由的history和hash模式


**路由的history模式和hash模式的区别**


hash模式在地址栏上有# ：localhost:8080/home ，history模式地址栏中没有#


配置路由模式 `mode : 'history'`


```javascript
const router = new Router({
    mode: 'history',
    routes: [
        {
            name: 'myhome',
            path: '/home',
            component: Home,
            meta: { isAuth: true },
        }
    ]
})
```


**history模式刷新出现404**


在hash模式下，前端路由修改的是#中的信息，而浏览器请求时是不带#后面的。


在history模式下，当刷新时，如果服务器中没有相应的响应或者资源localhost:8080/home，就会出现404


**解决history模式刷新出现404**


将前端项目部署到nginx中，在nginx配置


```
location / {
  try_files $uri $uri/ /index.html;
}
```
        
