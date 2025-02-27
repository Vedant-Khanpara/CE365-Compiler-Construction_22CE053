#include <iostream>
#include <vector>
#include <unordered_map>
#include <string>
using namespace std;

struct FiniteAutomaton {
    int numStates;
    vector<int> acceptingStates;
    int initialState;
    unordered_map<int, unordered_map<char, int>> transitions;

    // Constructor to initialize the FA
    FiniteAutomaton(int states, int initial, const vector<int>& accepts)
        : numStates(states), initialState(initial), acceptingStates(accepts) {}

    void addTransition(int fromState, char symbol, int toState) {
        transitions[fromState][symbol] = toState;
    }

    bool isAccepting(int state) {
        for (int acceptState : acceptingStates) {
            if (state == acceptState) {
                return true;
            }
        }
        return false;
    }

    bool validateString(const string& input) {
        int currentState = initialState;

        for (char c : input) {
            if (transitions[currentState].find(c) == transitions[currentState].end()) {
                return false;
            }
            currentState = transitions[currentState][c];
        }
        return isAccepting(currentState);
    }
};

int main() {
    int numSymbols = 2;
    cout << "Number of input symbols : " << numSymbols << endl;

    char symbols[2] = {'a', 'b'};
    cout << "Input symbols : ";
    for (int i = 0; i < numSymbols; ++i) {
        cout << symbols[i] << " ";
    }
    cout << endl;

    int numStates;
    cout << "Enter number of states : ";
    cin >> numStates;

    int initialState;
    cout << "Initial state : ";
    cin >> initialState;

    int numAcceptingStates;
    cout << "Number of accepting states : ";
    cin >> numAcceptingStates;

    vector<int> acceptingStates(numAcceptingStates);
    cout << "Accepting states : ";
    for (int i = 0; i < numAcceptingStates; ++i) {
        cin >> acceptingStates[i];
    }

    FiniteAutomaton fa(numStates, initialState, acceptingStates);

    cout << "Transition table :" << endl;
    for (int i = 0; i < numStates; ++i) {
        for (int j = 0; j < numSymbols; ++j) {
            char symbol = symbols[j];
            int toState;
            cout << i + 1 << " to " << symbol << " -> ";
            cin >> toState;
            fa.addTransition(i + 1, symbol, toState);  // Add transition to the FA
        }
    }

    string inputString;
    cout << "Input string : ";
    cin >> inputString;

    if (fa.validateString(inputString)) {
        cout << "Valid string" << endl;
    } else {
        cout << "Invalid string" << endl;
    }
    return 0;
}
