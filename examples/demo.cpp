#include<iostream>
#include<vector>
// #include<variant>

#define BASE_CLASS virtual public Object

class Object {
    std::string type = "object";
    public:
        virtual std::string toString() {
            return "Object[" + this->type + "]";
        }

        virtual ~Object() = default;

        virtual void setType(std::string type) final {
            this->type = type;
        }

        virtual std::string getType() final { return this->type; }

        virtual Object* add(Object* rightHand) {
            std::cout << "Invalid expression operation" << std::endl;
            std::exit(1);
        }

        virtual std::vector<Object*> getIterable() {
            std::cout << this->type + " is not iterable" << std::endl;
            std::exit(1);
        }
};

class Integer : BASE_CLASS {
    long long value;
    public:
        Integer(long long value) : value(value) { Object::setType("Integer"); }

        std::string toString() {
            return std::to_string(this->value);
        }
};

class String : BASE_CLASS {
    std::string value;
    public:
    String(std::string value) : value(value) { Object::setType("String"); }

    std::string toString() {
        return this->value;
    }
};

class Double : BASE_CLASS {
    long double value;
    public:
    Double(long double value) : value(value) { Object::setType("Double"); }

    std::string toString() {
        return std::to_string(value);
    }
};

class List : BASE_CLASS {
    std::vector<Object*> values;
    public:
    List(std::vector<Object*> values) : values(values) { Object::setType("List"); }
    std::string toString() {
        std::string s = "[";
        for (Object* item : this->values) {
            s += item->toString() + ", ";
        }
        if (!values.empty()) s.erase(s.size() - 2);
        s += "]";
        return s;
    }

    std::vector<Object*> getIterable() {
        return this->values;
    }
};

class CustomClass : BASE_CLASS {
    public: CustomClass() { Object::setType("CustomClass"); }
};

class ParentClass : BASE_CLASS {};
class ChildClass : public ParentClass, BASE_CLASS {
    std::string toString() {
        return "This is from child class";
    }
};

// function example
void print(Object* data) {
    std::cout << data->toString() << std::endl;
}

std::string type(Object* data) {
    return data->getType();
}

int main() {
    Object* data = new Integer(3LL);
    print(data);
    delete data;

    data = new String("Ashwin");
    print(data);
    delete data;

    data = new Double(3.14L);
    print(data);
    delete data;

    data = new List({new Integer(11), new String("Ashwin")});
    print(data);
    for(Object* item : data->getIterable()) {
        print(item);
    }
    delete data;

    data = new CustomClass();
    print(data);
    delete data;

    data = new ParentClass();
    print(data);
    delete data;

    data = new ChildClass();
    print(data);
    delete data;
    return 0;
}

/*
equalant
class CustomClass {}
class ParentClass {}
class ChildClass extends ParentClass {}

function main() {
    data = 3;
    print(data);

    data = "Ashwin";
    print(data);

    data = 3.14;
    print(data);

    data = [11, "Ashwin"];
    print(data);
    for item in data {
        print(item);
    }

    data = new CustomClass();
    print(data);

    data = new ParentClass();
    print(data);

    data = new ChildClass();
    print(data);
}
*/