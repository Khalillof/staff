
(($, Q) => {
    "use strict"; // Start of use strict

    document.addEventListener("DOMContentLoaded", function () {
        var _doc = document, topBtn = Q('#scroll-to-top'), BaseModel = $('#BaseModel'), BaseLogout = $("#logout");
        window.BaseModel = BaseModel || [];
        window.BaseLogout = BaseLogout || [];
        

        // initiate fastclick
        FastClick.attach(document.body);



        ///////////////////////////////////////////////////////////////////////////////////////////
        // Smooth scrolling using jQuery easing
        $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function () {
            if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
                var target = $(this.hash);
                target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
                if (target.length) {
                    $('html, body').animate({
                        scrollTop: (target.offset().top - 54)
                    }, 1000, "easeInOutExpo");
                    return false;
                }
            }
        });

        // Closes responsive menu when a scroll trigger link is clicked
        $('.js-scroll-trigger').click(function () {
            $('.navbar-collapse').collapse('hide');
        });

        // Activate scrollspy to add active class to navbar items on scroll
        $('body').scrollspy({
            target: '#mainNav',
            offset: 56
        });

        // Collapse Navbar
        let navbarCollapse = function () {
            if ($("#mainNav").offset().top > 100) {
                Q("#mainNav").addClass("navbar-shrink");
            } else {
                Q("#mainNav").removeClass("navbar-shrink");
            }
        };
        // Collapse now if page is not at top
        navbarCollapse();
        // Collapse the navbar when page is scrolled
        $(window).scroll(navbarCollapse);


        ///////////////////////////////////////////////////////////////////////////////////////////
        // Scroll to top button appear
        //// sort scroll                      
        window.scroll({ behavior: "smooth" });
        window.onscroll = function () { return _doc.body.scrollTop > 400 || _doc.documentElement.scrollTop > 400 ? topBtn.show() : topBtn.hide(); }
        //topBtn.E.onclick = () => Q(bdy).I("scrollTo", 0, 500);

        if (navigator.share) {
            _doc.getElementsByClassName("do-sharing")[0].innerHTML = "<button id='shareIcon' class='btn btn-warning'><span class='oi oi-share-boxed'></span> Share </button>";

            _doc.getElementById("shareIcon").addEventListener("click", (event) => {
                event.preventDefault();

                navigator.share({
                    title: _doc.title,
                    text: "Prof Drivers Ltd, Home for elite team of professional drivers.",
                    url: window.location.href
                }).then(() => {
                    console.log('Thanks for sharing!');
                }).catch(err => { console.log("we could not share because:", err.message); });

            }, false);
        }

        function common(e) {
            if (!Q(e.target).I("sorted")) {
                e.preventDefault();
                e.stopPropagation();
            }
        }

        ////////////
        Inputmask().mask(document.querySelectorAll("input"));

        //Initialize custom file input
        bsCustomFileInput.init();
        //$(this).bootstrapSwitch('state', $(this).prop('checked'));

        //Initialize Select2 Elements
        //$('.select2').select2();
        $('select').select2({
            theme: 'bootstrap4',
        });
        /////////////////
        Q('.needs-validation').on("submit", function (event) {
            let _form = event.target;

            if (!_form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                for (let i = 0; i < _form.elements.length; i++)
                    Q(_form.elements[i]).I("checkedUp")
            }
            else if (grecaptcha) {
                if (grecaptcha.getResponse().length === 0) {
                    event.preventDefault();
                    event.stopPropagation();
                    _form.insertAdjacentHTML("afterbegin", "<div class='alert alert-danger alert-dismissible' role='alert'><button type='button' class='close' data-dismiss='alert' aria-label='Close'><span aria-hidden='true'>&times;</span></button> Check the box I am Not robot </div>")
                    return;
                }

            }

            _form.classList.add('was-validated');
        });

        Q("*form").L && Q(".stepper").I("media", "stepper");

        Q("*select").on("change", common);
        Q("*textarea").on("change", common);

        Q("*input").on("change", common);

        $(".addPar").click(function (ee) {
            var elm = ee.target;
            var parName = elm.getAttribute("par");
            $.ajax({
                type: "GET",
                url: "/pars?s=" + parName, success: function (result) {
                    alert(result);
                    // $(elm).html(result);
                }
            });
        })
        //instantiate slideshows and concent

        //Q(".carousel").I("media","carousel");
        Q("#cookieConsent").I("concent");

        BaseModel.click(function (e) {
            let id = e.target.id;
            if (BaseLogout.length && id === "session-keep")
                app.session.keepAlive(); //Remove the warning dialog etc
            else if (BaseLogout.length && id === "session-logout")
                app.session.logout();

        });
        //BaseModel.on('hide.bs.modal', function (event) {
        //});
        BaseModel.on('show.bs.modal', function (event) {

            let buttonLink = $(event.relatedTarget); // Button that triggered the modal
            let _relatedTargetData = buttonLink.data('whatever'); // Extract info from data-* attributes
            // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
            // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.

            let mm = Q(BaseModel)
            if (_relatedTargetData)
                switch (_relatedTargetData) {
                    case "one":
                        mm.I("model", "School Bus", "<p class='item-intro text-muted'>Lorem ipsum dolor sit amet consectetur.</p> <img class='img-fix' src='/static/agency/images/310_170/van9.png' alt=''>  <p> Use this area to describe your project. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Est blanditiis dolorem culpa incidunt minus dignissimos deserunt repellat aperiam quasi sunt officia expedita beatae cupiditate, maiores repudiandae, nostrum, reiciendis facere nemo!</p> <ul class='list-inline'><li>Date: January 2017</li><li>Client: Threads</li><li>Category: Illustration</li></ul>");
                        break;
                    case "two":
                        mm.I("model", "Bus Couches", "<p class='item-intro text-muted'>Lorem ipsum dolor sit amet consectetur.</p> <img class='img-fix' src='/static/agency/images/310_170/couch_1.jpg' alt=''>  <p>Use this area to describe your project. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Est blanditiis dolorem culpa incidunt minus dignissimos deserunt repellat aperiam quasi sunt officia expedita beatae cupiditate, maiores repudiandae, nostrum, reiciendis facere nemo!</p> <ul class='list-inline'><li>Date: January 2017</li><li>Client: Threads</li><li>Category: Illustration</li></ul>");
                        break;
                    case "three":
                        mm.I("model", "Trucks", " <p class='item-intro text-muted'>Lorem ipsum dolor sit amet consectetur.</p> <img class='img-fix' src='/static/agency/images/310_170/truck_2.jpg' alt=''>  <p>Use this area to describe your project. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Est blanditiis dolorem culpa incidunt minus dignissimos deserunt repellat aperiam quasi sunt officia expedita beatae cupiditate, maiores repudiandae, nostrum, reiciendis facere nemo!</p> <ul class='list-inline'><li>Date: January 2017</li><li>Client: Threads</li><li>Category: Illustration</li></ul>");
                        break;
                    case "four":
                        mm.I("model", "Van TRuck ", " <p class='item-intro text-muted'>Lorem ipsum dolor sit amet consectetur.</p> <img class='img-fix' src='/static/agency/images/310_170/truck_1.jpg' alt=''>  <p>Use this area to describe your project. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Est blanditiis dolorem culpa incidunt minus dignissimos deserunt repellat aperiam quasi sunt officia expedita beatae cupiditate, maiores repudiandae, nostrum, reiciendis facere nemo!</p> <ul class='list-inline'><li>Date: January 2017</li><li>Client: Threads</li><li>Category: Illustration</li></ul>");
                        break;
                    case "five":
                        mm.I("model", "Professional Nurses", "<p class='item-intro text-muted'>Lorem ipsum dolor sit amet consectetur.</p> <img class='img-fix' src='/static/agency/images/nurse.jpg' alt=''>  <p>Use this area to describe your project. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Est blanditiis dolorem culpa incidunt minus dignissimos deserunt repellat aperiam quasi sunt officia expedita beatae cupiditate, maiores repudiandae, nostrum, reiciendis facere nemo!</p> <ul class='list-inline'><li>Date: January 2017</li><li>Client: Threads</li><li>Category: Illustration</li></ul>");
                        break;
                    case "six":
                        mm.I("model", "Professionals", "<p class='item-intro text-muted'>Lorem ipsum dolor sit amet consectetur.</p> <img class='img-fix' src='/static/agency/images/avatar.png' alt=''>  <p>Use this area to describe your project. Lorem ipsum dolor sit amet, consectetur adipisicing elit. Est blanditiis dolorem culpa incidunt minus dignissimos deserunt repellat aperiam quasi sunt officia expedita beatae cupiditate, maiores repudiandae, nostrum, reiciendis facere nemo!</p> <ul class='list-inline'><li>Date: January 2017</li><li>Client: Threads</li><li>Category: Illustration</li></ul>");
                        break;
                }

        })

        /// use session
        SetAppSession();



        // ((page)=> {
        //     return page === "/apply/drv" || "/apply/cnd" || "/info/create" && Q(".stepper").I("media", "stepper");
        //})(window.location.pathname);

    }, false); // document content loaded
})(jQuery, Q);

function SetAppSession() {
    // You could pull this out to its own file very easily
    window.app = window.app || {};

    app.session = {
        //Settings
        smodel: function (_type) {
            let mm = Q(BaseModel);
            if (_type === "Warning") {
                let bb = "<p> You've been inactive for a while. For your security, we'll log you out automatically. Click 'Stay Online' to continue your session. </p> <p>Your session will expire in <span class='font-weight-bold' id='sessionSecondsRemaining'>120</span> seconds. </p>";
                mm.I("model", "Session Expiration Warning", bb, "</br><div class='w-100'><button type='button' class='btn btn-primary float-left' id='session-keep' data-dismiss='modal'> Stay Online </button> <button  type='button' id='session-logout' class='btn btn-secondary float-right'  data-dismiss='modal'>logout</button></div>");
            } else if (_type === "LoggedOut") {
                mm.I("model", "logout alert", "You have been logged out", "<br> <button id='session-logout-display' type='button' class='btn btn-secondary float-right'  data-dismiss='modal'>close</button>");
            }
                
        },
        helper: {
            once: false,
            counter: 0
        },
        warningTimeout: 40000, //(ms) The time we give them to say they want to stay signed in
        inactiveTimeout: 80000, //(ms) The time until we display a warning message
        minWarning: 10000, //(ms) If they come back to page (on mobile), The minumum amount, before we just log them out
        timerSyncId: "SomethingUnique", //The key idleTimer will use to write to localStorage
        logoutUrl: "/Account/logout", //Your url to log out, if you want you could build the url to pass a referal param
        keepAliveUrl: "api/user/KeepAlive", // The url for the keepalive api
        keepaliveInterval: 5000, //(ms) the interval to call keep alive url
        //From here down you shouldnt have to alter anything
        warningStart: null, //Date time the warning was started
        warningTimer: null, //Timer running every second to countdown to logout
        keepaliveTimer: null, //Timer for independent ping to keep session alive
        logout: function () {
            //Write to storage to tell other tab its time to sign out
            if (typeof (localStorage) !== "undefined") {
                localStorage.setItem(app.session.timerSyncId, 0);
            }

            if (app.session.helper.counter <= 1) {
                app.session.helper.counter = app.session.helper.counter + 1;
                if (app.session.helper.counter >= 2) {
                    if (BaseLogout.length) {
                        BaseLogout[0].click();
                       document.location.pathname = app.session.logoutUrl;
                    }
                    else if (app.session.logoutUrl) {
                        window.location.pathname = app.session.logoutUrl;
                        app.session.smodel("LoggedOut");
                    } else {
                        window.location.pathname = "";
                    }
                    $(document).idleTimer("destroy"); // stop every thing
                }

            } else {
                return;
            }
            
             
            
        },
        keepAlive: function () {
            
            //Hide logout modal
          //  $("#mdlExpirationWarning").modal("hide");
            
            //Clear the timer
            clearTimeout(app.session.warningTimer);
            app.session.warningTimer = null;

            //Restart the idleTimer
            $(document).idleTimer("reset");
        },
        startKeepAliveTimer: function () {
            // Basically I just poll the server half way through the session life
            // to make sure the servers session stays valid
            clearTimeout(app.session.keepaliveTimer);
            app.session.keepaliveTimer = setInterval(function () {
                app.session.sendKeepAlive();
            }, (app.session.inactiveTimeout / 2));
        },
        sendKeepAlive: function () {
            // Write a new date to storage so any other tabs are informed that this tab
            //  sent the keepalive
            if (typeof (localStorage) !== "undefined") {
                localStorage.setItem(app.session.timerSyncId + "_keepalive", +new Date());
            }

            // The actual call to the keep alive api
            //$.post(app.session.keepAliveUrl).fail(function (jqXHR) {
            //    if (jqXHR.status == 500 || jqXHR.status == 0) {
            //        app.session.logout();
            //    }
            //});
        },
        showWarning: function (obj) {
            //Get time when user was last active
            let diff = (+new Date()) - obj.lastActive - obj.timeout,
                warning = (+new Date()) - diff;

            // Destroy idleTimer so users are forced to click the extend button
            $(document).idleTimer("pause");

            //On mobile js is paused, so see if this was triggered while we were sleeping
            if (diff >= app.session.warningTimeout || warning <= app.session.minWarning) {
                app.session.logout();
            } else {
                 app.session.smodel("Warning");
                //Show dialog, and note the time
                let _updateTime = $('#sessionSecondsRemaining');
               
                _updateTime.html(Math.round((app.session.warningTimeout - diff) / 1000));
                //$("#mdlExpirationWarning").modal("show");
                
                app.session.warningStart = (+new Date()) - diff;

                //Update counter downer every second
                app.session.warningTimer = setInterval(function () {
                    let remaining = Math.round((app.session.warningTimeout / 1000) - (((+new Date()) - app.session.warningStart) / 1000));

                    if (remaining >= 0) {
                        _updateTime.html(remaining);
                    } else {
                        app.session.logout();
                    }
                }, 1000)
            }
        },
        localWrite: function (e) {

            if (typeof (localStorage) !== "undefined" && e.originalEvent.key == app.session.timerSyncId && app.session.warningTimer != null) {
                // If another tab has written to cache then
                if (e.originalEvent.newValue == 0) {
                    // If they wrote a 0 that means they chose to logout when prompted
                    app.session.logout();
                } else {
                    // They chose to stay online, so hide the dialog
                    app.session.keepAlive();
                }

            } else if (typeof (localStorage) !== "undefined" && e.originalEvent.key == app.session.timerSyncId + "_keepalive") {
                // If the other tab sent a keepAlive poll to the server, reset the time here so we dont send two updates
                // This isnt really needed per se but it will save some server load
                app.session.startKeepAliveTimer();
            }
        },
        init: function () {
                console.log("logout session init function fired");

                //This will fire at X after page load, to show an inactive warning
                $(document).on("idle.idleTimer", function (event, elem, obj) {
                    app.session.showWarning(obj);
                });

                //Create a timer to keep server session alive, independent of idleTimer
                app.session.startKeepAliveTimer();

                //Set up the idleTimer, if inactive for X seconds log them out
                $(document).idleTimer({
                    timeout: app.session.inactiveTimeout - app.session.warningTimeout,
                    timerSyncId: app.session.timerSyncId
                });

                // Monitor writes by other tabs
                $(window).bind("storage", app.session.localWrite);
        }
    };

    /////////////////////

    return BaseLogout.length ? app.session.init() : false;
}



