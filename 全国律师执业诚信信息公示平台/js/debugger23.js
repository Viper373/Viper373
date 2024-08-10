function de2() {
//去除无限debugger
    Function.prototype.__constructor_back = Function.prototype.constructor
    Function.prototype.constructor = function () {
        if (arguments && typeof arguments[0] === 'string') {
            // alert("new function: “+ arguments[0]);
            if ("debugger" === arguments[0]) {
                // arguments[0] = "consoLe.Log(\"anti debugger\");";
                // arguments[0] = ";";
                return
            }
        }
        return Function.prototype.__constructor_back.apply(this, arguments)
    }
}

function de3() {
    var _Function = Function;
    Function = function (s) {
        if (s == "debugger") {
            console.log(s);
            return null;
        }
        return _Function(s);
    }
}