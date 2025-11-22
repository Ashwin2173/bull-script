VERSION = 1
INCLUDES = ["iostream", "vector", "chrono", "unordered_map"]
OBJECT = """
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
      std::cout << "Invalid usage of + for " << getType() << " and " << rightHand->getType() << std::endl;
      std::exit(1);
    }
    virtual Object* sub(Object* rightHand) {
      std::cout << "Invalid usage of - for " << getType() << " and " << rightHand->getType() << std::endl;
      std::exit(1);
    }
    virtual Object* mul(Object* rightHand) {
      std::cout << "Invalid usage of * for " << getType() << " and " << rightHand->getType() << std::endl;
      std::exit(1);
    }
    virtual Object* div(Object* rightHand) {
      std::cout << "Invalid usage of / for " << getType() << " and " << rightHand->getType() << std::endl;
      std::exit(1);
    }
    virtual Object* grt(Object* rightHand) {
      std::cout << "Invalid usage of > for " << getType() << " and " << rightHand->getType() << std::endl;
      std::exit(1);
    }
    virtual Object* gre(Object* rightHand) {
      std::cout << "Invalid usage of >= for " << getType() << " and " << rightHand->getType() << std::endl;
      std::exit(1);
    }
    virtual Object* lsr(Object* rightHand) {
      std::cout << "Invalid usage of < for " << getType() << " and " << rightHand->getType() << std::endl;
      std::exit(1);
    }
    virtual Object* lse(Object* rightHand) {
      std::cout << "Invalid usage of <= for " << getType() << " and " << rightHand->getType() << std::endl;
      std::exit(1);
    }
    virtual Object* equals(Object* rightHand);
    virtual Object* negate() {
      std::cout << "Can't negate " << getType() << std::endl;
      std::exit(1);
    }
    virtual std::vector<Object*> getIterable() {
      std::cout << this->type + " is not iterable" << std::endl;
      std::exit(1);
      }
};
class String; class Double; class Integer;"""
INTEGER = """
class Integer : BASE_CLASS {
    public:
    long long value;
    Integer(long long value) : value(value) { Object::setType("Integer"); }
    std::string toString() { return std::to_string(this->value); }
    Object* negate() override { return new Integer(-this->value); }
    Object* add(Object*) override;
    Object* sub(Object*) override;
    Object* mul(Object*) override;
    Object* div(Object*) override;
    Object* grt(Object*) override;
    Object* gre(Object*) override;
    Object* lsr(Object*) override;
    Object* lse(Object*) override;
    Object* equals(Object*) override;
};static std::unordered_map<long long, Integer*> INTEGER_POOL;"""
DOUBLE = """
class Double : BASE_CLASS {
    public:
    long double value;
    Double(long double value) : value(value) { Object::setType("Double"); }
    std::string toString() { return std::to_string(value); }
    Object* negate() override { return new Double(-this->value); }
    Object* add(Object*) override;
    Object* sub(Object*) override;
    Object* mul(Object*) override;
    Object* div(Object*) override;
    Object* grt(Object*) override;
    Object* gre(Object*) override;
    Object* lsr(Object*) override;
    Object* lse(Object*) override;
    Object* equals(Object*) override;
};static std::unordered_map<long double, Double*> DOUBLE_POOL;
"""
STRING = """
class String : BASE_CLASS {
    public:
    std::string value;
    String(std::string value) : value(value) { Object::setType("String"); }
    std::string toString() { return this->value; }
    Object* add(Object*) override;
    Object* equals(Object*) override;
};static std::unordered_map<std::string, String*> STRING_POOL;
"""
BOOLEAN = """
class Boolean : BASE_CLASS {
    public:
    bool value;
    Boolean(bool value) : value(value) { Object:: setType("Boolean"); }
    std::string toString() { return value ? "true" : "false"; }
    Object* equals(Object* other) override;
    Object* grt(Object*) override;
    Object* gre(Object*) override;
    Object* lsr(Object*) override;
    Object* lse(Object*) override;
};
Object* Object::equals(Object* other) { return new Boolean(false); }
static Boolean* TRUE = new Boolean(true);
static Boolean* FALSE = new Boolean(false);"""
DEFAULT_TYPE_POST_FUNCTION = """
Integer* get_int(long long v) {
    auto it = INTEGER_POOL.find(v);
    if (it != INTEGER_POOL.end()) return it->second;
    Integer* obj = new Integer(v);
    INTEGER_POOL.emplace(v, obj);
    return obj;
}
Double* get_double(long double v) {
    auto it = DOUBLE_POOL.find(v);
    if (it != DOUBLE_POOL.end()) return it->second;
    Double* obj = new Double(v);
    DOUBLE_POOL.emplace(v, obj);
    return obj;
}
String* get_string(const std::string& s) {
    auto it = STRING_POOL.find(s);
    if (it != STRING_POOL.end()) return it->second;
    String* obj = new String(s);
    STRING_POOL.emplace(s, obj);
    return obj;
}
Object* String::add(Object* other) { 
    if (auto obj = dynamic_cast<String*>(other)) {
        return new String(value + obj->value);
    } else if (auto obj = dynamic_cast<Integer*>(other)) {
        return new String(value + obj->toString());
    } else if (auto obj = dynamic_cast<Double*>(other)) {
        return new String(value + obj->toString());
    }
    return Object::add(other);
}
Object* Integer::add(Object* other) {
    if (auto obj = dynamic_cast<String*>(other)) {
        return new String(this->toString() + obj->value);
    } else if (auto obj = dynamic_cast<Integer*>(other)) {
        return new Integer(value + obj->value);
    } else if (auto obj = dynamic_cast<Double*>(other)) {
        return new Double(value + obj->value);
    }
    return Object::add(other);
}
Object* Double::add(Object* other) {
    if (auto obj = dynamic_cast<String*>(other)) {
        return new String(this->toString() + obj->value);
    } else if (auto obj = dynamic_cast<Integer*>(other)) {
        return new Double(value + obj->value);
    } else if (auto obj = dynamic_cast<Double*>(other)) {
        return new Double(value + obj->value);
    }
    return Object::add(other);
}
Object* Integer::sub(Object* other) {
    if (auto obj = dynamic_cast<Integer*>(other)) {
        return new Integer(value - obj->value);
    } else if (auto obj = dynamic_cast<Double*>(other)) {
        return new Double(value - obj->value);
    }
    return Object::sub(other);
}
Object* Double::sub(Object* other) {
    if (auto obj = dynamic_cast<Integer*>(other)) {
        return new Double(value - obj->value);
    } else if (auto obj = dynamic_cast<Double*>(other)) {
        return new Double(value - obj->value);
    }
    return Object::sub(other);
}
Object* Integer::mul(Object* other) {
    if (auto obj = dynamic_cast<Integer*>(other)) {
        return new Integer(value * obj->value);
    } else if (auto obj = dynamic_cast<Double*>(other)) {
        return new Double(value * obj->value);
    }
    return Object::mul(other);
}
Object* Double::mul(Object* other) {
    if (auto obj = dynamic_cast<Integer*>(other)) {
        return new Double(value * obj->value);
    } else if (auto obj = dynamic_cast<Double*>(other)) {
        return new Double(value * obj->value);
    }
    return Object::mul(other);
}
Object* Integer::div(Object* other) {
    if (auto obj = dynamic_cast<Integer*>(other)) {
        return new Integer(value / obj->value);
    } else if (auto obj = dynamic_cast<Double*>(other)) {
        return new Double(value / obj->value);
    }
    return Object::div(other);
}
Object* Double::div(Object* other) {
    if (auto obj = dynamic_cast<Integer*>(other)) {
        return new Double(value / obj->value);
    } else if (auto obj = dynamic_cast<Double*>(other)) {
        return new Double(value / obj->value);
    }
    return Object::div(other);
}
Object* Integer::grt(Object* other) {
    if (auto obj = dynamic_cast<Integer*>(other)) {
        return new Boolean(value > obj->value);
    } else if (auto obj = dynamic_cast<Double*>(other)) {
        return new Boolean(value > obj->value);
    }
    return Object::div(other);
}
Object* Double::grt(Object* other) {
    if (auto obj = dynamic_cast<Integer*>(other)) {
        return new Boolean(value > obj->value);
    } else if (auto obj = dynamic_cast<Double*>(other)) {
        return new Boolean(value > obj->value);
    }
    return Object::div(other);
}
Object* Integer::gre(Object* other) {
    if (auto obj = dynamic_cast<Integer*>(other)) {
        return new Boolean(value >= obj->value);
    } else if (auto obj = dynamic_cast<Double*>(other)) {
        return new Boolean(value >= obj->value);
    }
    return Object::div(other);
}
Object* Double::gre(Object* other) {
    if (auto obj = dynamic_cast<Integer*>(other)) {
        return new Boolean(value >= obj->value);
    } else if (auto obj = dynamic_cast<Double*>(other)) {
        return new Boolean(value >= obj->value);
    }
    return Object::div(other);
}
Object* Integer::lsr(Object* other) {
    if (auto obj = dynamic_cast<Integer*>(other)) {
        return new Boolean(value < obj->value);
    } else if (auto obj = dynamic_cast<Double*>(other)) {
        return new Boolean(value < obj->value);
    }
    return Object::div(other);
}
Object* Double::lsr(Object* other) {
    if (auto obj = dynamic_cast<Integer*>(other)) {
        return new Boolean(value < obj->value);
    } else if (auto obj = dynamic_cast<Double*>(other)) {
        return new Boolean(value < obj->value);
    }
    return Object::div(other);
}
Object* Integer::lse(Object* other) {
    if (auto obj = dynamic_cast<Integer*>(other)) {
        return new Boolean(value <= obj->value);
    } else if (auto obj = dynamic_cast<Double*>(other)) {
        return new Boolean(value <= obj->value);
    }
    return Object::div(other);
}
Object* Double::lse(Object* other) {
    if (auto obj = dynamic_cast<Integer*>(other)) {
        return new Boolean(value <= obj->value);
    } else if (auto obj = dynamic_cast<Double*>(other)) {
        return new Boolean(value <= obj->value);
    }
    return Object::div(other);
}
Object* Boolean::gre(Object* other) {
    if (auto obj = dynamic_cast<Boolean*>(other)) {
        return new Boolean(value == obj->value);
    } 
    return Object::div(other);
}
Object* Boolean::grt(Object* other) {
    if (auto obj = dynamic_cast<Boolean*>(other)) {
        return new Boolean(false);
    } 
    return Object::div(other);
}
Object* Boolean::lse(Object* other) {
    if (auto obj = dynamic_cast<Boolean*>(other)) {
        return new Boolean(value == obj->value);
    } 
    return Object::div(other);
}
Object* Boolean::lsr(Object* other) {
    if (auto obj = dynamic_cast<Boolean*>(other)) {
        return new Boolean(false);
    } 
    return Object::div(other);
}
Object* String::equals(Object* other) {
    if (auto obj = dynamic_cast<String*>(other)) {
        return new Boolean(value == obj->value);
    } 
    return Object::equals(other);
}
Object* Double::equals(Object* other) {
    if (auto obj = dynamic_cast<Double*>(other)) {
        return new Boolean(value == obj->value);
    } 
    return Object::equals(other);
}
Object* Integer::equals(Object* other) {
    if (auto obj = dynamic_cast<Integer*>(other)) {
        return new Boolean(value == obj->value);
    } 
    return Object::equals(other);
}
Object* Boolean::equals(Object* other) {
    if (auto obj = dynamic_cast<Boolean*>(other)) {
        return new Boolean(value == obj->value);
    } 
    return Object::equals(other);
}
"""
DEFAULT_FUNCTIONS = """
void print(Object* data) {
    std::cout << data->toString() << std::endl;
}
Object* type(Object* data) {
    return new String(data->getType());
}
Object* now() {
    return new Double(std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::system_clock::now().time_since_epoch()).count());
}"""
MAIN_FUNCTION = """
int main() {
Object* value = main_();
std::cout << "Exited with exit code " << value->toString() << std::endl;
return 0;
}"""