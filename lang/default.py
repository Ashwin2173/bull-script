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
      std::cout << "Invalid expression operation" << std::endl;
      std::exit(1);
    }
    virtual std::vector<Object*> getIterable() {
      std::cout << this->type + " is not iterable" << std::endl;
      std::exit(1);
      }
};"""
INTEGER = """
class Integer : BASE_CLASS {
    long long value;
    public:
    Integer(long long value) : value(value) { Object::setType("Integer"); }
    std::string toString() {
        return std::to_string(this->value);
    }
};"""
PRINT = """
void print(Object* data) {
    std::cout << data->toString() << std::endl;
}"""
MAIN_FUNCTION = """
int main() {
Object* value = main_();
print(value);
return 0;
}"""