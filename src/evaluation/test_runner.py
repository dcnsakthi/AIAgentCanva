"""
Test runner for agent evaluation
"""
from typing import Dict, Any, List
from datetime import datetime
import re

class TestRunner:
    """Run tests against agents"""
    
    def __init__(self, project: Dict[str, Any]):
        self.project = project
    
    def run_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single test case"""
        
        try:
            # Get agent
            agent_name = test_case['agent']
            agent = next(
                (a for a in self.project.get('agents', []) if a['name'] == agent_name),
                None
            )
            
            if not agent:
                return {
                    'test_name': test_case['name'],
                    'passed': False,
                    'error': f"Agent '{agent_name}' not found"
                }
            
            # Execute conversation
            responses = []
            
            for turn in test_case['conversation']:
                if turn['role'] == 'user':
                    # Simulate agent response
                    response = self._simulate_agent_response(agent, turn['content'])
                    responses.append(response)
            
            # Run assertions
            assertion_results = []
            for assertion in test_case['assertions']:
                result = self._check_assertion(assertion, responses)
                assertion_results.append(result)
            
            # Determine if test passed
            passed = all(assertion_results)
            
            return {
                'test_name': test_case['name'],
                'passed': passed,
                'assertion_results': assertion_results,
                'responses': responses,
                'timestamp': datetime.now().isoformat()
            }
        
        except Exception as e:
            return {
                'test_name': test_case['name'],
                'passed': False,
                'error': str(e)
            }
    
    def _simulate_agent_response(self, agent: Dict[str, Any], message: str) -> str:
        """Simulate agent response (in production, would call actual agent)"""
        return f"Response from {agent['name']}: Processed '{message}'"
    
    def _check_assertion(self, assertion: Dict[str, Any], responses: List[str]) -> bool:
        """Check if assertion passes"""
        
        assertion_type = assertion['type']
        expected_value = assertion['value']
        
        # Combine all responses for checking
        combined_response = " ".join(responses)
        
        if assertion_type == 'contains':
            return expected_value.lower() in combined_response.lower()
        
        elif assertion_type == 'not_contains':
            return expected_value.lower() not in combined_response.lower()
        
        elif assertion_type == 'equals':
            return combined_response.strip() == expected_value.strip()
        
        elif assertion_type == 'matches_regex':
            return bool(re.search(expected_value, combined_response))
        
        elif assertion_type == 'length_greater_than':
            return len(combined_response) > int(expected_value)
        
        elif assertion_type == 'length_less_than':
            return len(combined_response) < int(expected_value)
        
        else:
            return False
    
    def run_test_suite(self, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Run multiple test cases"""
        
        results = []
        
        for test_case in test_cases:
            result = self.run_test(test_case)
            results.append(result)
        
        passed_count = len([r for r in results if r['passed']])
        failed_count = len([r for r in results if not r['passed']])
        
        return {
            'total': len(results),
            'passed': passed_count,
            'failed': failed_count,
            'pass_rate': (passed_count / len(results) * 100) if results else 0,
            'results': results,
            'timestamp': datetime.now().isoformat()
        }
