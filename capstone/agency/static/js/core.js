(function (window) {
    var _doc = document;

    window.requestAnimationFrame =
        window.requestAnimationFrame ||
        window.webkitRequestAnimationFrame ||
        window.mozRequestAnimationFrame ||
        window.msRequestAnimationFrame ||
        function (f) { return window.setTimeout(f, 1000 / 60); };

    window.cancelAnimationFrame =
        window.cancelAnimationFrame ||
        window.webkitCancelAnimationFrame ||
        window.mozCancelAnimationFrame ||
        window.msCancelAnimationFrame ||
        function (requestId) { clearTimeout(requestId); };

    function attach(_slcter) {
        // find elements
        var selectorType = '';

        function r(a) {
            selectorType = a;
            _slcter = _slcter.substring(1, _slcter.length);
        }
        switch (_slcter.charAt(0)) {
            case "#": r('getElementById');
                break;
            case ".": r('getElementsByClassName');
                break;
            case "*": r('getElementsByTagName');
                break;
            case "!": r('querySelector');
                break;
            default: selectorType = 'querySelectorAll';
        }

        return document[selectorType](_slcter) || [];
    }

    function getDocScrollTop() {
        // IE8 used `document.documentElement`
        return document.documentElement && document.documentElement.scrollTop || document.body.scrollTop;

    }
    function setDocScrollTop(value) {

        window.scrollTo(0, value);

        return value;
    }
    function _trigger(_Qe, _event, _fun) {
        const t = _Qe, ee = t.E;
        function _process() {
            return t.split(_event).forEach(function (v) {
                var event = new CustomEvent(v, { bubbles: true, cancelable: true });
                typeof ee.addEventListener === "function" ? ee.addEventListener(v, _fun, false) : ee.attachEvent('on' + v, _fun);
                ee.dispatchEvent(event);
            });
        }
        if (typeof window.CustomEvent === "function") {
            _process();
        } else {
   
                function CustomEvent(event, params) {
                    params = params || { bubbles: false, cancelable: false, detail: undefined };
                    var evt = document.createEvent('CustomEvent');
                    evt.initCustomEvent(event, params.bubbles, params.cancelable, params.detail);
                    return evt;
                }

                CustomEvent.prototype = window.Event.prototype;

                window.CustomEvent = CustomEvent;
           
            _process();
        }
    }
    function isfun(fun) {
        return fun && typeof fun === 'function' ? fun() : fun;
    }
    function ms(_qe) {
        this.Qe = _qe;
    }

    function IQ(_slct) {
        const rst = _slct && typeof _slct === "string" ? attach(_slct) : _slct, _length = rst.length ? rst.length : rst.tagName ? 1 : 0;
        this.E = rst;
        this.L = _length;
    }

    IQ.prototype = {
        I: function (name, arg1, arg2, arg3, arg4) {
            return name ? new ms(this)[name](arg1, arg2, arg3, arg4) : false;             
        },
        isfun: function (fun) {
            var t = this;
            fun && typeof fun === 'function' ? fun.call(t) : fun;
            return t;
            
           
        },
        cssvalue: function (_cssproperty, _property) {
            if (!_property) _property = null;
            var elm = this.E;
            var reslt = window.getComputedStyle(elm, null).getPropertyValue(_cssproperty);
            // console.log(reslt);
            return reslt;
        },
        time: function (fun, _time) {
            window.setTimeout(fun, _time);
            return this;
        },
        Interval: function (fun, _time) {
            var clr = window.setInterval(function () {fun; clearTimeout(clr) }, _time);
            return this;
        },
        before: function (_html) {
            this.E.insertAdjacentHTML("beforeend", _html);
            return this;
        },
        after: function (_html) {
            this.E.insertAdjacentHTML("afterend", _html); 
            return this;

        },
        each: function (fun) {
            Array.prototype.filter.call(this.E, fun);
            return this;
        },
        loop: function (fun) {
            let i = 0, t = this;
            for (i; i < t.L; i++)
                fun.call(t, t.E[i], i);
            return t;
        },
        on: function (_events, _fun) {
            const t = this;
            return t.loop(function (_e) {
                t.split(_events).forEach(function (n) {
                    typeof _e.addEventListener === "function" ? _e.addEventListener(n, _fun, false) : _e.attachEvent('on' + n, _fun);
                });
            });
        },
        off: function (_event, _handller) {
            this.E.removeEventListener(_event, _handller, false);
            return this;
        },
        find: function (names, fun) {
            const t = this;
            t.split(names).forEach(function (n, i) {
                switch (n.charAt(0)) {
                    case ".":
                        fun.call(t, t.E.querySelectorAll(n), i);// classes
                        break;
                    case "#":
                        fun.call(t, t.E.querySelector(n), i);// id
                        break;
                    case "*":
                        fun.call(t, t.E.querySelectorAll(n.substring(1, n.length)), i); // group elements
                        break;
                    case "!":
                        fun.call(t, t.E.querySelector(n.substring(1, n.length)), i); // first element
                        break;
                    default: t.E.querySelectorAll(n).forEach(fun); // all but one after one
                }
            });
            return t;
        },
        split: function (_names) {
            return _names.split(/[ ,]+/);
        },
        animate: function (_classes, fun) {
            const t = this, _elm = t.E, cc = _classes, _animation = t.animationEnd();
            t.show().addClass(_classes);

            _elm.addEventListener(_animation, handler, false);
            function handler() {
                t.off(_animation, handler).removeClass(cc);
                void _elm.offsetWidth; // triggering reflow / the actual magic
                //t.isfun(fun);
                if (fun && typeof fun === 'function') fun.call(t);
            }
            return t;
        },
        animationEnd: function () {
            const anims = {
                animation: 'animationend',
                OAnimation: 'oAnimationEnd',
                MozAnimation: 'mozAnimationEnd',
                WebkitAnimation: 'webkitAnimationEnd',
                ////transition
                transition: 'transitionend',
                OTransition: 'oTransitionEnd',
                MozTransition: 'mozTransitionEnd',
                WebkitTransition: 'webkitTransitionEnd'
            };

            for (let a in anims) {
                if (this.E.style[a] !== undefined) {
                    return anims[a];
                }
            }
        },
        show: function () { return this.css("opacity", 1).css("display", "initial"); },
        hide: function () { return this.css("opacity", 0).css("display", "none"); },
        fadeOut: function () {
            return this.show().animate("animate__animated, animate__fadeOut", function () { this.hide() });
        },
        fadeIn: function () {
            return this.hide().animate("animate__animated, animate__fadeIn", function () { this.show() });
        },
        css: function (_css, _value) { this.E.style[_css] = _value; return this; },
        removeElms: function () { return this.each((e) => e.parentNode.removeChild(e)); },
        addClass: function (_classes) {
            let t = this;
            t.split(_classes).forEach((c) => t.mcss('add', c, () => !t.hasClass(c) ? t.E.className += " " + c : null));
            return t;
        },
        clearClass: function (_class) {
            _class ? this.E.className = _class : this.E.className = "";
            return this;
        },
        hasClass: function (_className) {
            let t = this;
            return t.mcss('contains', _className, () => new RegExp(_className).test(t.E.className));

        },
        hasClsCase: function (clsn) { return this.E.className.indexOf(clsn) > -1 ? true : false; },
        toggle: function (_classname) {
            let t = this;
            t.mcss('toggle', _classname, () => t.hasClass(_classname) ? t.removeClass(_classname) : t.addClass(_classname));
            return t;
        },
        removeAddClass: function (_remove, _add) {
            return this.removeClass(_remove).addClass(_add);
        },
        removeClass: function (_classes) {
            let t = this;
            t.split(_classes).forEach(function (_class) {

                t.mcss('remove', _class, function () {
                    if (t.hasClass(_class)) {
                        let reg = new RegExp('(\\s|^)' + _class + '(\\s|$)');
                        t.E.className = t.E.className.replace(reg, ' ');
                    }
                })
            });
            return t;
        },
        mcss: function (name, arg, fun) {
            let t = this, clst = t.classList;
            return clst ? clst[name](arg) : typeof fun === 'function' ? fun.apply(t) : fun;
        }

    };

    function Q(_selector) {
        return _selector ? new IQ(_selector) : new IQ();
    }

    ms.prototype = {
        notice: function (_noticeTitle, _noticeBody, _reload) {
            return _notice(_noticeTitle, _noticeBody, _reload);
        },
        Script: function (url) {
            var script = _doc.createElement('script');
            script.type = 'text/javascript';
            script.src = url;
            script.async = true;
            script.defer = true;
            script.onerror = function () {
                // console.log(new Error("Failed to load" + url));
            };
            this.Qe.E.appendChild(script);

        },
        Style: function (url) {
            var style = _doc.createElement('link');
            style.setAttribute('type', 'text/css');
            style.setAttribute('rel', 'stylesheet');
            style.setAttribute('type', 'text/css');
            style.setAttribute('href', url);
            style.onerror = function () {
                // console.log(new Error("Failed to load" + url));
            };
            this.Qe.E.appendChild(style);

        },
        cook:{
            // var cookie = readCookie('WeUse-cookie-msg');
            // setCookie('WeUse-cookie-msg', 'yes', 60, "/");

            // Read cookie
   
                read: function (name) {
                    var nameEQ = name + "=";
                    var decodedCookie = decodeURIComponent(document.cookie);
                    var ca = decodedCookie.split(';');
                    for (var i = 0; i < ca.length; i++) {
                        var c = ca[i];
                        while (c.charAt(0) === ' ') {
                            c = c.substring(1);
                        }
                        if (c.indexOf(nameEQ) == 0) {
                            return c.substring(nameEQ.length, c.length);
                        }
                }
                return null; 
                },
                // Set cookie
                set: function (name, value, days, path) {
                    if (days) {
                        var date = new Date();
                        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
                        var expires = "expires=" + date.toUTCString();
                        _doc.cookie = name + "=" + value + ";" + expires + "; path=" + path;
                    }
                }
            
        },
        trigger: function (_event, _fun) {
            return _trigger(this.IQ, _event, _fun);
        },
        Reg: function (_type, _val) {
            return _Reg.call(this,_type, _val);
        },
        checkedUp: function () {
            return _checkedUp.call(this);
        },
        sorted: function () {
            return _sorted.call(this);
        },
        AJAXSubmit: function (oFormElement, callback) {
            return AJAXSubmit.call(this,oFormElement, callback)
        },
        scrollTo: function (to = 0, duration = 16) {

            if (duration < 0) {
                return;
            }
            const diff = to - getDocScrollTop();

            if (diff === 0) {
                return;
            }
            const perTick = diff / duration * 10;
            requestAnimationFrame(() => {
                if (Math.abs(perTick) > Math.abs(diff)) {
                    setDocScrollTop(getDocScrollTop() + diff);
                    return;
                }

                setDocScrollTop(getDocScrollTop() + perTick);
                if (diff > 0 && getDocScrollTop() >= to || diff < 0 && getDocScrollTop() <= to) {
                    return;
                }

                this.scrollTo(to, duration - 16);
            });
        },
        model: function (_title, _body, btn) {

            if (!_body) return;
            
            var _mdl = this.Qe.E || BaseModel, _title = _title || "Alert", btn = btn || "<button id='BaseMdlbtn' class='btn btn-primary' data-dismiss='modal' type='button'> <i class='fas fa-times'></i> Close Project </button>";
            var _Mbody = "<h3 class='text-center'>" + _title + "</h3> <hr/>" + _body + "<hr/>" + btn;

                _mdl.find('.modal-body').html(_Mbody);
                _mdl.modal("show");            
        },
        concent: function () {
            return _concent.call(this);
        },
        ready: function (_fun) {
            document.onreadystatechange = function () {
                ////loaded
                if (document.readyState === 'complete')
                    return _fun();
                //else if (document.readyState === 'interactive')
                //    _fun();
            };
        },
        media: function (_name) {
            this.Qe.each(function (a) {
                if (_name === "stepper") requestAnimationFrame(() => new stepper(a));
                else if (_name === "carousel") requestAnimationFrame(() => new carousel(a));
            });
        }
    };

    function _concent() {
        let _t = this.Qe, cooc = this.cook.read(".AspNet.Consent");
        
        if (!cooc) {
            return _t.E ? _t.animate("animate__animated, animate__slideInDown, animate__delay-5s").find("![data-cookie-string],#closeConsent", function (el, i) {

                if (i === 0) {
                    el.onclick = function () { _doc.cookie = el.dataset.cookieString; _consenthander(); };
                } else if (i === 1) {
                    el.onclick = () => _consenthander();
                }

                var _consenthander = function () {
                    return _t.animate("animate__animated, animate__slideOutUp", () => _t.hide());
                };
            }) : false;
        } else {
            return false;
        }
    }
    async function AJAXSubmit(oFormElement, callback) {
        // var resultElement = oFormElement.elements.namedItem("g-recaptcha");

        if (!oFormElement.checkValidity()) {
            for (var i = 0; i < oFormElement.elements.length; i++)
                Q(oFormElement.elements[i]).I("checkedUp")
            return;
        }
        else if (grecaptcha) {
            if (grecaptcha.getResponse().length === 0) {
                oFormElement.insertAdjacentHTML("afterbegin", "<div class='alert alert-danger alert-dismissible' role='alert'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button> Check the box I am Not robot </div>")
                return;
            }
        }

        const formData = new FormData(oFormElement);
        var responseFormatedTex = "";

        if (window.fetch) {
            try {
                const response = await fetch(oFormElement.action, {
                    method: "POST",
                    body: formData
                });
                if (responce.ok) {
                    window.location.href = "/";
                }
                responseFormatedTex = "Result: " + response.status + " " + response.statusText;
                if (callback) callback.call(this, response, responseFormatedTex)
                console.log(responseFormatedTex);

            } catch (error) {
                console.error("Error : ", error)
            }
        } else {
            try {
                var oReq = new XMLHttpRequest();
                oReq.onload = function (e) {
                    responseFormatedTex = 'Result: ' + this.status + ' ' + this.statusText;
                    console.log(responseFormatedTex);
                };
                oReq.open("post", oFormElement.action);
                oReq.send(formData);

                if (callback) callback.call(this, oReq.status, responseFormatedTex)

            } catch (error) {
                console.error("Error : ", error)
            }

        }
    }

    function _Reg(_type, _val) {
        switch (_type) {
            case "postcode":
                return /^((([A-PR-UWYZ][0-9])|([A-PR-UWYZ][0-9][0-9])|([A-PR-UWYZ][A-HK-Y][0-9])|([A-PR-UWYZ][A-HK-Y][0-9][0-9])|([A-PR-UWYZ][0-9][A-HJKSTUW])|([A-PR-UWYZ][A-HK-Y][0-9][ABEHMNPRVWXY]))\s?([0-9][ABD-HJLNP-UW-Z]{2})|(GIR)\s?(0AA))$/.test(_val.toUpperCase()) ? "" : "enter a valid UK PostCode";
            case "mobile":
                let number = _val;
                number = number.replace(/\(|\)|\s+|-/g, "");
                //var test = number.length > 9 && number.match(reg.mobile);
                return number.length > 9 && number.match(/^(?:(?:(?:00\s?|\+)44\s?|0)7(?:[1345789]\d{2}|624)\s?\d{3}\s?\d{3})$/) ? "" : "enter valid UK mobile number";
            case "tel":
                return /^(?:(?:(?:00\s?|\+)44\s?|0)(?:1\d{8,9}|[23]\d{9}|7(?:[1345789]\d{8}|624\d{6})))$/.test(_val) ? "" : "enter valid UK number";
            case "text":
                // /^[a-zA-Z0-9]+$/.test(_val) ? "" : "text and numbers only";
                //^[A-Za-z0-9 _]*[A-Za-z0-9][A-Za-z0-9 _]*$    "text and numbers and space only";
                return /^[A-Za-z0-9 _]*[A-Za-z0-9][A-Za-z0-9 _]*$/.test(_val) ? "" : "text numbers and space only";
            case "textarea":
                return !(/[^A-Za-z0-9 .'?!,@$#-_]/).test(_val) ? "" : "text and numbers only";
            case "date":
                return /^\d{1,2}\/\d{1,2}\/\d{4}$/.test(_val) ? "" : "this format dd/mm/yyyy";
            case "email":
                return /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(_val) ? "" : "valid email eg: aa@aa.com";
            case "password":
                return /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,10}/.test(_val) ? "" : "8 to 10 chars 1 uppercase lowercase number and special char";
        }
    }
    function _checkedUp() {
        let t = this.Qe, _elm = t.E, nx = _elm.nextElementSibling, has = nx ? nx.className.indexOf("invalid-feedback") > -1 ? true : false : false;
        if (!_elm.validity.valid) {
            if (has) {
                nx.innerHTML = _elm.validationMessage;
            } else {
                t.after("<div class='invalid-feedback'>" + _elm.validationMessage + "</div>");
            }
            t.removeAddClass("is-valid", "is-invalid");
            return false;
        } else {
            if (has) {
                nx.innerHTML = "";
            }
            t.removeAddClass("is-invalid", "is-valid");
            return true;
        }
    }
    function _sorted() {
        let tt = this, t = tt.Qe, _elm = t.E, tagname = _elm.tagName.toLowerCase(), _type, val;
        function one(i) {
            _elm.setCustomValidity(tt.Reg(i, val));
        }

        if (tagname === "input") {
            _type = _elm.getAttribute("type").toLowerCase(), val = _elm.value;
            switch (_type) {
                case "text":
                    _elm.id.toLowerCase() === "postcode" ? one("postcode") : one(_type);
                    break;
                case "radio":
                    if (t.hasClsCase("inpt-pres")) {
                        switch (_elm.id) {
                            case "Disqualified":
                                tt.notice("alert", "this position rquire you to have a clean driving history", true);
                                break;
                            case "LessThanSixPoint2":
                                tt.notice("alert", "you must have UK/EU full driving licence with less than 6 point", true);
                                break;
                            case "RightToWork2":
                                tt.notice("Alert", "you must have right to work in the UK", true);
                                break;
                        }
                    }
                    break;
                case "tel":
                    _elm.id.toLowerCase() === "mobile" ? one("mobile") : one(_type);
                    break;
                case "file":
                    _elm.setCustomValidity(checkfile(_elm));
                    break;
                case "email":
                    one(_type);
                    break;
                case "password":
                    var _frmId = _elm.form.id;
                    if (_frmId === "registerform" && _elm.id === "RgCnPassword") {
                        var _test = tt.Reg(_type, val);
                        if (_test === "") {
                            var password = _elm.form.querySelector('input[name="Input.Password"]');
                            password.value !== _elm.value ? _elm.setCustomValidity("Passwords Don't Match") : _elm.setCustomValidity("");

                        } else {
                            _elm.setCustomValidity(_test);
                        }
                        break;

                    }

                    if (_frmId === "loginform" || _frmId === "forgetpassword" || _frmId === "Tow-factor") {
                        break;
                    } else {
                        one("password");
                    }

                    break;
            }
        }
        else if (tagname === "textarea") {
            val = _elm.value;
            one("textarea");
        }

        return tt.checkedUp();
    }
    function checkfile(_elm, _filesNo = 2) {
        let files = _elm.files, _flength = files.length, _i = 0, _file, _type;


        if (!files || _flength === 0) {
            return `doesn't contain any files.`;
            //throw new Error(`Element ${_file.name} doesn't contain any files.`);
        }

        if (_flength > _filesNo) return _flength + " files selcted ? only" + _filesNo + " two files";

        for (_i; _i < _flength; _i++) {
            _file = _elm.files[_i];
            _type = _file.type;

            if (_file.name.length > 50) return _file.name + "name is too long ";
            //else if (_type !== "application/pdf") return _type + ":not accepted only pdf files";
            else if (_type !== "application/pdf" && _type !== "image/jpeg" && _type !== "image/png" && _type !== "image/jpg") return _type + ": only images and pdf files";
          else if (_file.size / 2048 / 2048 > 2) return _file.name + ": size is exceeds 4 MB";
          // else if (_file.size / 1024 / 1024 > 2) return _file.name + ": size is exceeds 2 MB";

        }

        return "";
    }
    function _notice(_noticeTitle, _noticeBody, _reload = false) {

        let ee = Q("#notice");

        if (!ee.L) {
            let _html = "<div id='notice' class='notice'><div id='notice-content' class='notice-content text-center'><button type='button' class='closeNotice close red'> <span aria-hidden='true'>&times;</span></button><span class='h11' data-heading='Important Notice'><span data-heading='Important Notice'>Important Notice</span></span><br><h5 class='NoticeTitle'>" + _noticeTitle + "</h5> <div class='p-2 noticeBody'>" + _noticeBody + "</div><br><button type='button' class='closeNotice btn btn-warning btn-sm '>Close</button></div></div>";
            _doc.body.insertAdjacentHTML("beforeend", _html);
            ee = Q("#notice");
        } else {
            ee.find(".NoticeTitle , .noticeBody", function (e, i) {
                if (i === 0) { e[0].innerHTML = _noticeTitle; }
                else if (i === 1) { e[0].innerHTML = _noticeBody };
            });
        }

        return ee.animate("animate__animated, animate__slideInDown").find(".closeNotice", function (el) {
            el.forEach((e) => e.onclick = function () {
                return ee.animate("animate__animated, animate__slideOutUp", function () { ee.hide(); if (_reload) _doc.location.reload(true); });
            });
        });
    }

    ///stepper()
    class stepper { 
        constructor(_parent) {
            if (!_parent) return false;
            const T = this;
            this.crntTabNo = 0;
            this.parent = Q(_parent) || [];
            this.tabers = [];
            this.steps = [];
            this.preBtn = null;
            this.nexBtn = null;

            T.parent.find(".taber,.nextBtn,.prevBtn", function (_obj, idx) {
                switch (idx) {
                    case 0:
                        T.tabers = _obj;
                        var _steps_pa = document.createElement("div");
                        _steps_pa.className = "tabersteps";
                        T.tabers.forEach((e, i) => _steps_pa.insertAdjacentHTML("beforeend", "<span  class='step'>" + i + "</li>"));
                        T.parent.E.insertAdjacentElement("afterbegin", _steps_pa);
                        T.steps = _steps_pa.children;
                        break;
                    case 1:
                        T.nexBtn = _obj[0];
                        T.nexBtn.onclick = () => T.NextPrev(1);
                        break;
                    case 2:
                        T.preBtn = _obj[0];
                        T.preBtn.onclick = () => T.NextPrev(-1);
                        break;
                }

            });
            
            this.ShowTaber(this.crntTabNo);
            // this.parent.fadeIn();
        }

        ShowTaber(n) {
            // This function will display the specified taber of the form ...
            const t = this, x = t.tabers;
            Q(x[n]).fadeIn();

            // ... and fix the Previous/Next buttons:
            n === 0 ? t.preBtn.disabled = true : t.preBtn.disabled = false;

            if (n === (x.length - 1)) {
                t.nexBtn.setAttribute("type", "submit");
                t.nexBtn.innerHTML = " Submit  <i class='fa fa-upload red'></i> ";

            }
            else {
                t.nexBtn.innerHTML = " Next  <i class='fa fa-arrow-circle-right'></i> ";
                t.nexBtn.setAttribute("type", "button");
            }
            // ... and run a function that displays the correct step indicator:
            t.Indicator(n);
        }

        NextPrev(n) {
            // This function will figure out which taber to display
            const t = this, x = t.tabers;
            // prevent hide on last taber submit:
            if (n === 1 && t.crntTabNo + n === x.length) {
                t.nexBtn.submit();
                   return false;
            }
            // Exit the function if any field in the current taber is invalid:
            if (n === 1 && !t.validator()) return false;

            // Hide the current taber 
                Q(x[t.crntTabNo]).hide();
            

            // Increase or decrease the current taber by 1:
            t.crntTabNo +=  n;
            // if you have reached the end of the form... :
            if (t.crntTabNo >= x.length) {
                //...the form gets submitted:
                t.nexBtn.submit();
                return false;
            }
            // Otherwise, display the correct taber:
            t.ShowTaber(t.crntTabNo);
        }

        validator() {
            // This function deals with validation of the form fields
            const t = this;
            var valid = true, _currenttabCache = [];

            Q(t.tabers[t.crntTabNo]).find("input,select,textarea", function (e) {
                if (!Q(e).I("checkedUp")) valid = false;
                _currenttabCache.push(e);
            });

            // If the valid status is true, mark the step as finished and valid:
            if (valid) {
                _currenttabCache.forEach(function (e, i, ar) {
                    Q(e).removeClass("is-valid");
                    delete ar[i];
                });
                Q(t.steps[t.crntTabNo]).addClass("finish");
            } else {
                Q(t.steps[t.crntTabNo]).removeClass("finish");
                t.Indicator(t.crntTabNo);
            }

            return valid;
        }

        Indicator(n) {
            // This function removes the "active" class of all steps...
            const x = this.steps;
            Q(x).loop((e) => Q(e).removeClass("active"));

            Q(x[n]).addClass("active");
        }
    }

    window.Q = Q;

})(window);
