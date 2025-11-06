"""
Evaluation page - Test and validate agents
"""
import streamlit as st
from typing import List, Dict, Any
import json
from datetime import datetime
from src.evaluation.test_runner import TestRunner
from src.evaluation.test_case import TestCase

def show():
    """Display evaluation page"""
    
    if not st.session_state.project:
        st.warning("No project loaded. Please create or load a project from the home page.")
        if st.button("Go to Home"):
            st.session_state.current_page = 'landing'
            st.rerun()
        return
    
    st.markdown("<h1 class='main-header'>✅ Evaluation Harness</h1>", unsafe_allow_html=True)
    st.markdown("Define and run tests to validate your agents")
    
    # Initialize test state
    if 'test_suites' not in st.session_state:
        st.session_state.test_suites = []
    if 'test_results' not in st.session_state:
        st.session_state.test_results = []
    
    # Tabs
    tabs = st.tabs(["📝 Test Cases", "▶️ Run Tests", "📊 Results"])
    
    with tabs[0]:
        show_test_cases()
    
    with tabs[1]:
        show_test_runner()
    
    with tabs[2]:
        show_test_results()

def show_test_cases():
    """Display test case management"""
    
    st.markdown("### Create Test Cases")
    st.markdown("Define scripted conversations with expected outcomes and assertions")
    
    with st.form("new_test_case"):
        test_name = st.text_input("Test Name", placeholder="e.g., Customer Greeting Test")
        
        test_description = st.text_area(
            "Description",
            placeholder="What does this test validate?",
            height=100
        )
        
        # Agent selection
        agents = st.session_state.project.get('agents', [])
        agent_names = [agent['name'] for agent in agents]
        
        selected_agent = st.selectbox(
            "Agent to Test",
            agent_names if agent_names else ["No agents available"]
        )
        
        # Conversation script
        st.markdown("#### Conversation Script")
        
        num_turns = st.number_input("Number of Turns", min_value=1, max_value=10, value=3)
        
        conversation = []
        for i in range(num_turns):
            st.markdown(f"**Turn {i+1}**")
            user_msg = st.text_input(f"User Message {i+1}", key=f"user_{i}")
            conversation.append({"role": "user", "content": user_msg})
        
        # Assertions
        st.markdown("#### Assertions")
        
        assertion_type = st.selectbox(
            "Assertion Type",
            ["contains", "not_contains", "equals", "matches_regex", "length_greater_than", "length_less_than"]
        )
        
        assertion_value = st.text_input("Expected Value")
        
        # Submit
        if st.form_submit_button("Create Test Case", use_container_width=True):
            if test_name and selected_agent and conversation:
                test_case = {
                    'id': f"test_{len(st.session_state.test_suites)}",
                    'name': test_name,
                    'description': test_description,
                    'agent': selected_agent,
                    'conversation': conversation,
                    'assertions': [{
                        'type': assertion_type,
                        'value': assertion_value
                    }],
                    'created_at': datetime.now().isoformat()
                }
                
                st.session_state.test_suites.append(test_case)
                st.success(f"Test case '{test_name}' created!")
                st.rerun()
            else:
                st.error("Please fill in all required fields")
    
    # Display existing test cases
    if st.session_state.test_suites:
        st.markdown("---")
        st.markdown("### Existing Test Cases")
        
        for test in st.session_state.test_suites:
            with st.expander(f"📋 {test['name']}"):
                st.markdown(f"**Description:** {test['description']}")
                st.markdown(f"**Agent:** {test['agent']}")
                st.markdown(f"**Turns:** {len(test['conversation'])}")
                st.markdown(f"**Assertions:** {len(test['assertions'])}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Edit", key=f"edit_{test['id']}"):
                        st.info("Edit functionality coming soon")
                
                with col2:
                    if st.button("Delete", key=f"delete_{test['id']}"):
                        st.session_state.test_suites = [
                            t for t in st.session_state.test_suites if t['id'] != test['id']
                        ]
                        st.rerun()

def show_test_runner():
    """Display test execution interface"""
    
    st.markdown("### Run Test Suite")
    
    if not st.session_state.test_suites:
        st.info("No test cases defined. Create test cases in the 'Test Cases' tab.")
        return
    
    # Select tests to run
    test_names = [test['name'] for test in st.session_state.test_suites]
    selected_tests = st.multiselect(
        "Select Tests to Run",
        test_names,
        default=test_names
    )
    
    # Run configuration
    col1, col2 = st.columns(2)
    
    with col1:
        parallel_execution = st.checkbox("Run tests in parallel", value=False)
    
    with col2:
        stop_on_failure = st.checkbox("Stop on first failure", value=False)
    
    # Run button
    if st.button("▶️ Run Tests", use_container_width=True, type="primary"):
        run_tests(selected_tests, parallel_execution, stop_on_failure)

def run_tests(test_names: List[str], parallel: bool, stop_on_fail: bool):
    """Execute selected tests"""
    
    st.markdown("### Test Execution")
    
    # Get selected test cases
    tests = [t for t in st.session_state.test_suites if t['name'] in test_names]
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    runner = TestRunner(st.session_state.project)
    results = []
    
    for idx, test in enumerate(tests):
        status_text.text(f"Running: {test['name']}...")
        
        try:
            result = runner.run_test(test)
            results.append(result)
            
            # Show result
            if result['passed']:
                st.success(f"✅ {test['name']} - PASSED")
            else:
                st.error(f"❌ {test['name']} - FAILED")
                st.text(result.get('error', 'Unknown error'))
            
            if not result['passed'] and stop_on_fail:
                st.warning("Stopping test execution due to failure")
                break
        
        except Exception as e:
            st.error(f"Error running test {test['name']}: {str(e)}")
            results.append({
                'test_name': test['name'],
                'passed': False,
                'error': str(e)
            })
        
        # Update progress
        progress_bar.progress((idx + 1) / len(tests))
    
    status_text.text("Test execution complete!")
    
    # Store results
    test_run = {
        'id': f"run_{datetime.now().timestamp()}",
        'timestamp': datetime.now().isoformat(),
        'results': results,
        'total': len(results),
        'passed': len([r for r in results if r['passed']]),
        'failed': len([r for r in results if not r['passed']])
    }
    
    st.session_state.test_results.append(test_run)
    
    # Summary
    st.markdown("---")
    st.markdown("### Summary")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Tests", test_run['total'])
    with col2:
        st.metric("Passed", test_run['passed'])
    with col3:
        st.metric("Failed", test_run['failed'])

def show_test_results():
    """Display test results and history"""
    
    st.markdown("### Test Results")
    
    if not st.session_state.test_results:
        st.info("No test results available. Run tests to see results.")
        return
    
    # Display latest results
    latest_run = st.session_state.test_results[-1]
    
    st.markdown(f"**Latest Run:** {latest_run['timestamp']}")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total", latest_run['total'])
    with col2:
        st.metric("Passed", latest_run['passed'])
    with col3:
        st.metric("Failed", latest_run['failed'])
    with col4:
        pass_rate = (latest_run['passed'] / latest_run['total'] * 100) if latest_run['total'] > 0 else 0
        st.metric("Pass Rate", f"{pass_rate:.1f}%")
    
    # Detailed results
    st.markdown("---")
    st.markdown("### Detailed Results")
    
    for result in latest_run['results']:
        status_icon = "✅" if result['passed'] else "❌"
        status_color = "green" if result['passed'] else "red"
        
        with st.expander(f"{status_icon} {result['test_name']}"):
            st.markdown(f"**Status:** :{status_color}[{'PASSED' if result['passed'] else 'FAILED'}]")
            
            if not result['passed']:
                st.markdown("**Error:**")
                st.code(result.get('error', 'Unknown error'))
            
            if 'details' in result:
                st.markdown("**Details:**")
                st.json(result['details'])
    
    # Export results
    st.markdown("---")
    if st.button("📥 Export Test Results", use_container_width=True):
        export_test_results(latest_run)

def export_test_results(test_run: Dict[str, Any]):
    """Export test results to JSON"""
    
    json_data = json.dumps(test_run, indent=2)
    
    st.download_button(
        label="Download Results",
        data=json_data,
        file_name=f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
        mime="application/json"
    )
