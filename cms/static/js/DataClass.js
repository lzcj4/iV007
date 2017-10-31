function Dictionary() {
    var items = {};

    this.has = function (key) {
        return key in items;
    };

    this.put = function (key, value) {
        items[key] = value;
    };

    this.remove = function (key) {
        if (this.has(key)) {
            delete items[key];
            return true;
        }
        return false;
    };

    this.get = function (key) {
        var result = this.has(key) ? items[key] : undefined;
        return result;
    };

    this.values = function () {
        var values = [];
        for (var k in items) {
            if (this.has(k)) {
                values.push(items[k]);
            }
        }
        return values;
    };

    this.clear = function () {
        items = {};
    };

    this.size = function () {
        var count = 0;
        for (var prop in items) {
            if (items.hasOwnProperty(prop)) {
                ++count;
            }
        }
        return count;
    };

    this.getItems = function () {
        return items;
    };
}

function DescObject(props) {
    this.desckey = props ? props.desckey : "";
    this.descvalue = props ? props.descvalue : "";
}

function RectObject(props) {
    if (!props) {
        return;
    }
    this.x = props.x;
    this.y = props.y;
    this.width = props.width;
    this.height = props.height;
    this.objid = props.objid;
    this.objtype = props.objtype;
    this.drawcolor = props.drawcolor;
    this.descs = new Array();
    for (var index in props.descs) {
        var item = props.descs[index];
        this.descs.push(new DescObject(item));
    }
}

function TimeObject(props) {
    if (!props) {
        return;
    }
    this.time = props.time;
    this.objects = new Array();
    for (var index in props.objects) {
        var item = props.objects[index];
        this.objects.push(new RectObject(item));
    }
    this.get = function (index) {
        if (index >= 0 && index < this.objects.length) {
            return this.objects[index];
        }
        return null;
    }
}

function mousePosition(ev) {
    var scrollLeft = document.documentElement.scrollLeft || document.body.scrollLeft;
    var scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
    return {
        x: ev.clientX + scrollLeft - document.documentElement.clientLeft,
        y: ev.clientY + scrollTop - document.documentElement.clientTop
    };
}



