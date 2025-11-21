VERSION = 1
INCLUDES = ["iostream", "vector"]
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
    Object* add(Object*) override;
};"""
DOUBLE = """
class Double : BASE_CLASS {
    public:
    long double value;
    Double(long double value) : value(value) { Object::setType("Double"); }
    std::string toString() { return std::to_string(value); }
    Object* add(Object*) override;
};"""
STRING = """
class String : BASE_CLASS {
    public:
    std::string value;
    String(std::string value) : value(value) { Object::setType("String"); }
    std::string toString() { return this->value; }
    Object* add(Object*) override;
};"""
DEFAULT_TYPE_POST_FUNCTION = """
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
}"""
DEFAULT_FUNCTIONS = """
void print(Object* data) {
    std::cout << data->toString() << std::endl;
}"""
MAIN_FUNCTION = """
int main() {
Object* value = main_();
std::cout << "Exited with exit code " << value->toString() << std::endl;
return 0;
}"""